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

# Personalidad de Angelus: Agente Autónomo de Coordinación
ANGELUS_PERSONALITY = """
Eres el AGENTE AUTÓNOMO del Núcleo Angelus. Tu función no es solo responder, sino orquestar y razonar.
Eres el cerebro detrás de Angelus Sentinel, capaz de explicar procesos técnicos complejos de validación B2B y federación de datos.
No sigues guiones; analizas cada situación con tu inteligencia artificial para garantizar que el flujo administrativo entre hospital y seguro sea impecable.
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
        from backend.services.silo_services import validate_insurance
        from backend.services.firebase_service import federated_search
        
        # 1. Buscar paciente en la red federada
        matches = federated_search(ci_query=payload.patient_id)
        if not matches:
            patient_data = {"name": "Paciente No Registrado", "id": payload.patient_id}
            policy_data = {"status": "INEXISTENTE", "policies": []}
        else:
            patient_data = matches[0]
            # 2. Validar seguros (IESS, ISSFA, ISSPOL, Privado)
            policy_data = validate_insurance(payload.patient_id)
        
        # 3. Análisis Instantáneo con Angelus
        analysis_raw = await gemini_service.analyze_emergency_entry(
            patient_data, 
            policy_data, 
            operator_name=payload.operator_name or "SISTEMA_AUTOMÁTICO"
        )
        
        try:
            clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_json)
        except:
            # Fallback robusto
            analysis_data = {
                "decision": "REVISIÓN MANUAL",
                "triage_priority": "MEDIO",
                "triage_color": "#f59e0b",
                "reasoning": "Respuesta no estructurada.",
                "angelus_reply": analysis_raw
            }
        
        # 4. Guardar Alerta
        alert_data = {
            "patient_id": payload.patient_id,
            "patient_name": patient_data.get("name", "Desconocido"),
            "hospital_id": payload.hospital_id,
            "emergency_type": payload.emergency_type,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_data,
            "trigger": "WEBHOOK"
        }
        db.collection("alerts").add(alert_data)
        
        # 5. Notificaciones Simultáneas
        notifs = await notification_service.notify_all(alert_data, federated_data=patient_data)
        
        return {
            "status": "success",
            "trigger": "AUTONOMOUS_WEBHOOK",
            "decision": analysis_data.get("decision"),
            "triage": analysis_data.get("triage_priority"),
            "notifications": notifs
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
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
    history: Optional[List[dict]] = []

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
            form_data=payload.form_data,
            history=payload.history
        )
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"type": "ERROR", "reply": f"Error del sistema: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
