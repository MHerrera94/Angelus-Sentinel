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

    async def pre_triage(self, symptoms: str):
        """
        Analiza los síntomas para dar una prioridad preliminar.
        """
        prompt = f"""
        {ANGELUS_PROMPT}
        Analiza estos síntomas de emergencia: "{symptoms}"
        Clasifica la prioridad (CRÍTICO, MEDIO, ESTABLE) y asigna un color (Rojo: #ef4444, Amarillo: #f59e0b, Verde: #10b981).
        Responde en JSON:
        {{"priority": "NIVEL", "reasoning": "Breve explicación", "color": "HEX_COLOR"}}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return {"priority": "ESTABLE", "reasoning": "Síntomas generales.", "color": "#10b981"}
        except:
            return {"priority": "ESTABLE", "reasoning": "Análisis preliminar no disponible.", "color": "#10b981"}

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
        # ... (código anterior se mantiene igual)
        """
        Analiza el ingreso de emergencia usando la personalidad de Angelus.
        """
        prompt = f"""
        {ANGELUS_PROMPT}
        
        INTERACCIÓN:
        Estás respondiendo al usuario: {operator_name}. Asegúrate de dirigirte a él/ella de forma personalizada en tu 'angelus_reply'.
        
        DATOS DEL CASO:
        - Paciente: {patient_data.get('name')} (Edad: {patient_data.get('age')})
        - Póliza: {policy_data.get('plan')} (Estado: {policy_data.get('status')})
        - Coberturas: {", ".join(policy_data.get('coverage', []))}
        - Exclusiones: {", ".join(policy_data.get('exclusions', []))}
        - Preexistencias: {", ".join(policy_data.get('pre_existing_conditions', []))}
        
        INSTRUCCIÓN:
        1. Analiza si el paciente tiene cobertura para este ingreso.
        2. Clasifica el nivel de TRIAGE basado en los síntomas/motivo (CRÍTICO, MEDIO, ESTABLE).
        3. Asigna un color (Rojo para Crítico, Amarillo para Medio, Verde para Estable).
        4. Detecta posibles conflictos o inconsistencias.
        5. Genera una respuesta JSON con:
           - decision: "APROBADO" | "REVISIÓN MANUAL" | "RECHAZADO"
           - triage_priority: "CRÍTICO" | "MEDIO" | "ESTABLE"
           - triage_color: "#ef4444" | "#f59e0b" | "#10b981"
           - reasoning: "Explicación técnica detallada"
           - angelus_reply: "Tu respuesta personalizada para {operator_name} (Sé sofisticado y directo)"
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error en la validación del Centinela: {str(e)}"

gemini_service = GeminiService()
