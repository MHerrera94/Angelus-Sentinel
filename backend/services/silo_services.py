from backend.services.firebase_service import db, federated_search, register_in_sentinel
from backend.services.notification_service import notification_service
import asyncio
from datetime import datetime

async def search_patients(query: str, search_type: str) -> dict:
    """
    Busca pacientes en las bases de datos federadas (Hospital Sentinel, IESS, Seguros Privados, MSP).
    """
    if search_type == 'ci':
        matches = federated_search(ci_query=query)
    else:
        matches = federated_search(name_query=query)
        
    return {"matches": matches, "count": len(matches)}

async def register_patient(ci: str, name: str, symptoms: str) -> dict:
    """
    Crea un nuevo registro de paciente en la base de datos local db_sentinel_hospital.
    """
    patient_data = {
        "id": ci,
        "name": name,
        "last_visit": datetime.now().strftime("%Y-%m-%d"),
        "pre_existing_conditions": []
    }
    result = register_in_sentinel(patient_data)
    return {"result": result, "patient": patient_data}

async def validate_insurance(ci: str) -> dict:
    """
    Verifica el estado de la póliza de un paciente en las bases de aseguradoras (IESS, ISSFA, ISSPOL, Privados).
    """
    matches = federated_search(ci_query=ci)
    if not matches:
        return {"status": "NO ENCONTRADA", "message": "Paciente no existe en silos."}
    
    patient = matches[0]
    policies = patient.get("insurance_policies", [])
    
    if policies:
        active_count = len([p for p in policies if p["status"] == "Activo"])
        return {
            "status": "VALIDADO", 
            "count": len(policies),
            "active_count": active_count,
            "policies": policies,
            "message": f"Se encontraron {len(policies)} pólizas vinculadas al paciente."
        }
    return {"status": "SIN SEGURO", "message": "No se encontraron pólizas activas en la red."}

async def send_admission_alert(ci: str, decision: str, triage_color: str, triage_priority: str = "NO ESPECIFICADO", symptoms: str = "No especificado") -> dict:
    """
    Envía una alerta de admisión al hospital y notifica a la aseguradora.
    Args:
        ci: Cédula de identidad del paciente.
        decision: Decisión administrativa ("APROBADO" | "REVISIÓN MANUAL" | "RECHAZADO").
        triage_color: Color del triaje asignado.
        triage_priority: Prioridad del triaje ("ALTA" | "MEDIA" | "BAJA").
        symptoms: Motivo de consulta o síntomas detectados.
    """
    matches = federated_search(ci_query=ci)
    patient_data = matches[0] if matches else {}
    
    alert_data = {
        "patient_id": ci,
        "patient_name": patient_data.get("name", "Desconocido"),
        "hospital_id": "SENTINEL-HOSP",
        "emergency_type": symptoms,
        "timestamp": datetime.now().isoformat(),
        "analysis": {
            "decision": decision, 
            "triage_color": triage_color, 
            "triage_priority": triage_priority,
            "symptoms": symptoms
        }
    }
    
    # Await directament el servicio de notificación
    await notification_service.notify_all(alert_data, federated_data=patient_data)
    
    return {"success": True, "message": "Notificaciones enviadas a Hospital y Seguro."}

# Lista de herramientas para inyectar en Gemini
SILO_TOOLS = [search_patients, register_patient, validate_insurance, send_admission_alert]
