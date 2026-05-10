import google.generativeai as genai
import json
import os
from backend.config import GEMINI_API_KEY, ANGELUS_PROMPT

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY no configurado en .env")

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-3.1-flash-lite')
        self.current_action = ""
        self.is_active = False

    async def pre_triage(self, symptoms: str):
        """
        Analiza la urgencia administrativa basada en el motivo de ingreso.
        """
        prompt = f"""
        {ANGELUS_PROMPT}
        Analiza este motivo de ingreso: "{symptoms}"
        Determina la URGENCIA ADMINISTRATIVA (ALTA, MEDIA, BAJA) para la validación de seguros.
        Asigna un color de alerta para el gestor (Rojo: #ef4444, Amarillo: #f59e0b, Verde: #10b981).
        Responde en JSON:
        {{"priority": "NIVEL", "reasoning": "Breve justificación administrativa", "color": "HEX_COLOR"}}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return {"priority": "BAJA", "reasoning": "Trámite administrativo estándar.", "color": "#10b981"}
        except:
            return {"priority": "BAJA", "reasoning": "Análisis administrativo no disponible.", "color": "#10b981"}

    async def extract_entities(self, raw_text: str):
        """
        Extrae el nombre del paciente y el motivo de la emergencia del texto libre.
        """
        # Usamos un prompt más directo y sin la personalidad para evitar distracciones
        prompt = f"""
        Identifica el nombre del paciente y el motivo de la emergencia en este texto: "{raw_text}"
        
        Responde ÚNICAMENTE en este formato JSON:
        {{"patient_name": "Nombre", "emergency_type": "Motivo", "hospital_name": "HOSP-01"}}
        
        Si no hay nombre, pon null en "patient_name".
        """
        try:
            response = await self.model.generate_content_async(prompt)
            text = response.text.strip()
            print(f"DEBUG - Angelus Raw Response: {text}")
            
            # Limpieza agresiva de JSON
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            return {"patient_name": None, "emergency_type": "General", "hospital_name": "HOSP-01"}
        except Exception as e:
            print(f"Error en extracción: {e}")
            return {"patient_name": None, "emergency_type": "General", "hospital_name": "HOSP-01"}

    async def analyze_emergency_entry(self, patient_data: dict, policy_data: dict, operator_name: str = "Gestor"):
        """
        Analiza el ingreso desde una perspectiva de cobertura y preexistencias.
        """
        prompt = f"""
        {ANGELUS_PROMPT}
        
        INTERACCIÓN:
        Estás respondiendo al Gestor: {operator_name}. Mantén un tono técnico y profesional.
        
        DATOS DE IDENTIDAD Y COBERTURA:
        - Paciente: {patient_data.get('name')} (Historial en Hospital: {'SI' if patient_data.get('id') else 'NO'})
        - Póliza: {policy_data.get('plan')} (Estado: {policy_data.get('status')})
        - Coberturas Activas: {", ".join(policy_data.get('coverage', []))}
        - Preexistencias Registradas: {", ".join(policy_data.get('pre_existing_conditions', []))}
        
        INSTRUCCIÓN PARA EL CENTINELA:
        1. Valida si la póliza está activa para el ingreso actual.
        2. Menciona si el paciente tiene preexistencias que el Gestor del Seguro deba conocer.
        3. Determina si el ingreso se aprueba automáticamente o requiere revisión manual por el Gestor.
        4. Genera una respuesta JSON con:
           - decision: "APROBADO" | "REVISIÓN MANUAL" | "RECHAZADO"
           - triage_priority: "ADMIN_ALTA" | "ADMIN_MEDIA" | "ADMIN_BAJA"
           - triage_color: "#ef4444" | "#f59e0b" | "#10b981"
           - reasoning: "Análisis de póliza y preexistencias"
           - angelus_reply: "Tu informe técnico para el Gestor {operator_name} sobre la validez del ingreso."
        """
        
        self.is_active = True
        self.current_action = "Analizando condiciones y coberturas del paciente..."
        try:
            response = await self.model.generate_content_async(prompt)
            self.is_active = False
            return response.text
        except Exception as e:
            self.is_active = False
            return f"Error en la validación administrativa: {str(e)}"

    async def orchestrate_emergency(self, user_message: str, operator_name: str, form_data: dict = None):
        """
        Orquesta la respuesta utilizando Function Calling (Manos y Dedos de la IA).
        """
        from backend.services.silo_services import SILO_TOOLS
        
        # Modelo configurado con herramientas
        model_with_tools = genai.GenerativeModel(
            model_name='gemini-3.1-flash-lite',
            tools=SILO_TOOLS,
            system_instruction=ANGELUS_PROMPT
        )
        
        chat = model_with_tools.start_chat()
        
        self.is_active = True
        self.current_action = "Procesando la solicitud..."
        
        context = f"El operador {operator_name} dice: {user_message}\n"
        if form_data:
            context += f"Datos del formulario provistos: {json.dumps(form_data)}\n"
            
        context += "Tu tarea es usar tus herramientas (search_patients, register_patient, validate_insurance) según corresponda. Al final, SIEMPRE DEBES LLAMAR A send_admission_alert(ci, decision, triage_color, triage_priority) antes de emitir tu respuesta final."
        
        # Enviar mensaje inicial
        response = await chat.send_message_async(context)
        
        # Bucle de ejecución de herramientas (max 3 iteraciones para evitar loops infinitos)
        for _ in range(3):
            if not response.parts:
                break
                
            found_fc = False
            for i, part in enumerate(response.parts):
                if hasattr(part, 'function_call') and part.function_call:
                    found_fc = True
                    fc = part.function_call
                    func_name = fc.name
                    func_args = dict(fc.args)
                    
                    print(f"DEBUG - Angelus llamó a herramienta: {func_name} con args {func_args}")
                    
                    action_map = {
                        "search_patients": "Buscando paciente en la red federada...",
                        "register_patient": "Registrando nuevo paciente en la base local...",
                        "validate_insurance": "Validando estado de póliza con aseguradora...",
                        "send_admission_alert": "Emitiendo alertas a canales de emergencia..."
                    }
                    self.current_action = action_map.get(func_name, f"Ejecutando {func_name}...")
                    
                    # Ejecutar la función correspondiente
                    tool_result = {"error": "Herramienta no encontrada"}
                    for tool in SILO_TOOLS:
                        if tool.__name__ == func_name:
                            try:
                                tool_result = tool(**func_args)
                            except Exception as e:
                                tool_result = {"error": str(e)}
                            break
                    
                    # Devolver el resultado al modelo
                    response = await chat.send_message_async(
                        {"function_response": {"name": func_name, "response": {"result": tool_result}}}
                    )
                    break
            
            if not found_fc:
                break
                
        # Extraer el texto final de forma segura
        final_text = ""
        for part in response.parts:
            if hasattr(part, 'text') and part.text:
                final_text += part.text
            elif hasattr(part, 'function_call') and part.function_call:
                final_text = f"El agente requiere realizar una acción ({part.function_call.name})."
                break
        
        if not final_text:
            final_text = "Procesamiento completado."
            
        # Pedimos a un modelo sin herramientas que estructure la respuesta final
        struct_prompt = f"""
        Convierte este reporte o pregunta de la IA en el siguiente formato JSON estricto:
        {final_text}
        
        Reglas de Tipo (type):
        - Usa "RESULT" si es un informe final o confirmación.
        - Usa "QUESTION" si necesitas que el usuario confirme algo (ej. "¿Desea registrar al paciente?").
        
        Formato requerido:
        {{
            "type": "RESULT" o "QUESTION",
            "reply": "El resumen ejecutivo o la pregunta directa para el operador.",
            "color": "#ef4444" (Rojo), "#f59e0b" (Amarillo), "#10b981" (Verde),
            "options": [{{"id": "cédula", "label": "SÍ, REGISTRAR EN SENTINEL"}}] (SOLO si type es QUESTION y ofreces una acción),
            "analysis": {{
                "decision": "ESTADO",
                "angelus_reply": "El texto detallado del reporte técnico"
            }}
        }}
        """
        struct_response = await self.model.generate_content_async(struct_prompt)
        self.is_active = False
        try:
            import re
            json_match = re.search(r'\{.*\}', struct_response.text, re.DOTALL)
            return json.loads(json_match.group(0))
        except:
            return {
                "type": "RESULT",
                "reply": final_text,
                "color": "#10b981",
                "analysis": {"decision": "PROCESADO", "angelus_reply": final_text}
            }

gemini_service = GeminiService()
