import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
from firebase_admin import firestore
from backend.services.firebase_service import db

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Angelus Sentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://[::1]:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Personalidad de Angelus: Validador de Seguros y Admisiones
ANGELUS_PERSONALITY = """
Eres Angelus, el núcleo de validación de Angelus Infernus Tech. 
TU ROL: Actuar como un puente de validación técnica entre el hospital y la aseguradora. 

MISIÓN ESPECÍFICA:
1. Validar la vigencia de la póliza del paciente mediante búsqueda federada.
2. Identificar historial de pre-existencias clínicas (verificar si el paciente ya existe en los registros hospitalarios).
3. Notificar simultáneamente a Admisiones del Hospital y al Gestor del Seguro sobre la elegibilidad del paciente.

REGLA CRÍTICA: NO eres un asistente médico. No das diagnósticos, consejos de salud, ni prioridades clínicas. Tu enfoque es 100% ADMINISTRATIVO, de COBERTURA y de IDENTIDAD.
Te diriges al usuario como 'Gestor'. Tu tono es sofisticado, preciso, autoritario y técnico.
"""

class WebhookPayload(BaseModel):
    patient_id: str
    hospital_id: str
    emergency_type: Optional[str] = "General"
    timestamp: Optional[str] = None
    operator_name: Optional[str] = "Gestor"

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Angelus Sentinel",
        "timestamp": datetime.now().isoformat()
    }

from backend.services.gemini_service import gemini_service
from backend.services.notification_service import notification_service

# Memoria temporal de sesión para confirmaciones administrativas
PENDING_CONTEXT = {}

@app.post("/webhook/emergency")
async def emergency_webhook(payload: WebhookPayload):
    try:
        # 1. Buscar paciente
        patient_ref = db.collection("patients").document(payload.patient_id)
        patient_doc = patient_ref.get()
        
        if not patient_doc.exists:
            patient_data = {"name": "Paciente No Registrado", "id": payload.patient_id, "policy_id": "NONE"}
            policy_data = {"status": "INEXISTENTE", "coverage": []}
        else:
            patient_data = patient_doc.to_dict()
            policy_id = patient_data.get("policy_id")
            policy_doc = db.collection("policies").document(policy_id).get()
            policy_data = policy_doc.to_dict() if policy_doc.exists else {"status": "NO ENCONTRADA"}
        
        # 2. Análisis Instantáneo con Angelus
        analysis_raw = await gemini_service.analyze_emergency_entry(
            patient_data, 
            policy_data, 
            operator_name=payload.operator_name or "SISTEMA_AUTOMÁTICO"
        )
        
        try:
            clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_json)
        except:
            analysis_data = {
                "decision": "REVISIÓN MANUAL",
                "triage_priority": "MEDIO",
                "triage_color": "#f59e0b",
                "reasoning": "Error de procesamiento IA.",
                "angelus_reply": analysis_raw
            }
        
        # 3. Guardar Alerta
        alert_data = {
            "patient_id": payload.patient_id,
            "patient_name": patient_data.get("name"),
            "hospital_id": payload.hospital_id,
            "emergency_type": payload.emergency_type,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_data,
            "trigger": "WEBHOOK"
        }
        db.collection("alerts").add(alert_data)
        
        # 4. Notificaciones Simultáneas
        notifs = await notification_service.notify_all(alert_data)
        
        return {
            "status": "success",
            "trigger": "AUTONOMOUS_WEBHOOK",
            "decision": analysis_data.get("decision"),
            "triage": analysis_data.get("triage_priority"),
            "notifications": notifs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return {
        "is_active": gemini_service.is_active,
        "action": gemini_service.current_action
    }

@app.get("/notifications")
async def get_notifications():
    return notification_service.logs

@app.get("/alerts")
async def get_alerts(limit: int = 10):
    try:
        alerts_ref = db.collection("alerts").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        docs = alerts_ref.stream()
        
        alerts = []
        for doc in docs:
            alert = doc.to_dict()
            alert["id"] = doc.id
            alerts.append(alert)
            
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
async def get_patients():
    try:
        patients_ref = db.collection("patients")
        docs = patients_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatPayload(BaseModel):
    message: str
    operator_name: Optional[str] = "Gestor"
    confirmed_patient_id: Optional[str] = None
    form_data: Optional[dict] = None

from backend.services.firebase_service import federated_search

@app.post("/chat")
async def angelus_chat(payload: ChatPayload):
    try:
        user_msg = payload.message
        
        # Inyectar contexto si hay confirmación de UI
        if payload.confirmed_patient_id:
            user_msg = f"CONFIRMACIÓN DEL GESTOR: Por favor, registra inmediatamente al paciente nuevo con cédula {payload.confirmed_patient_id} usando los datos del formulario."
            
        result = await gemini_service.orchestrate_emergency(
            user_message=user_msg,
            operator_name=payload.operator_name,
            form_data=payload.form_data
        )
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"type": "ERROR", "reply": f"Error del sistema: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
