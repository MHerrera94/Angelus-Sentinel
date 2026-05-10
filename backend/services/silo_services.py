from backend.services.firebase_service import db, federated_search, register_in_sentinel
from backend.services.notification_service import notification_service
import asyncio
from datetime import datetime

def search_patients(query: str, search_type: str) -> dict:
    """
    Busca pacientes en las bases de datos federadas (Hospital Sentinel, IESS, Seguros Privados, MSP).
    Args:
        query: El texto a buscar.
        search_type: El tipo de búsqueda ('name' para buscar por nombre, 'ci' para buscar por cédula).
    Returns:
        Un diccionario con los resultados agrupados por cédula.
    """
    if search_type == 'ci':
        matches = federated_search(ci_query=query)
    else:
        matches = federated_search(name_query=query)
        
    return {"matches": matches, "count": len(matches)}

def register_patient(ci: str, name: str, symptoms: str) -> dict:
    """
    Crea un nuevo registro de paciente en la base de datos local db_sentinel_hospital.
    Args:
        ci: Cédula de identidad del paciente.
        name: Nombre completo del paciente.
        symptoms: Síntomas o motivo de ingreso.
    Returns:
        Resultado de la operación.
    """
    patient_data = {
        "id": ci,
        "name": name,
        "last_visit": datetime.now().strftime("%Y-%m-%d"),
        "pre_existing_conditions": []
    }
    result = register_in_sentinel(patient_data)
    return {"result": result, "patient": patient_data}

def validate_insurance(ci: str) -> dict:
    """
    Verifica el estado de la póliza de un paciente en las bases de aseguradoras.
    Args:
        ci: Cédula de identidad del paciente.
    Returns:
        Información de la póliza.
    """
    matches = federated_search(ci_query=ci)
    if not matches:
        return {"status": "NO ENCONTRADA", "message": "Paciente no existe en silos."}
    
    patient = matches[0]
    policy = patient.get("insurance_policy")
    if policy:
        return {"status": policy.get("status", "ACTIVA"), "plan": policy.get("plan", "Básico")}
    return {"status": "SIN SEGURO", "message": "No se encontraron pólizas activas."}

def send_admission_alert(ci: str, decision: str, triage_color: str, triage_priority: str = "NO ESPECIFICADO") -> dict:
    """
    Envía una alerta de admisión al hospital y notifica a la aseguradora.
    Debe llamarse al finalizar la validación.
    Args:
        ci: Cédula de identidad del paciente.
        decision: Decisión administrativa ("APROBADO" | "REVISIÓN MANUAL" | "RECHAZADO").
        triage_color: Color del triaje asignado.
        triage_priority: Prioridad del triaje ("ALTA" | "MEDIA" | "BAJA").
    """
    matches = federated_search(ci_query=ci)
    patient_data = matches[0] if matches else {}
    
    alert_data = {
        "patient_id": ci,
        "patient_name": patient_data.get("name", "Desconocido"),
        "hospital_id": "SENTINEL-HOSP",
        "emergency_type": f"Admisión: {decision}",
        "timestamp": datetime.now().isoformat(),
        "analysis": {"decision": decision, "triage_color": triage_color, "triage_priority": triage_priority}
    }
    
    # notify_all es async, por lo que creamos una tarea
    loop = asyncio.get_event_loop()
    loop.create_task(notification_service.notify_all(alert_data, federated_data=patient_data))
    
    return {"success": True, "message": "Notificaciones enviadas a Hospital y Seguro."}

# Lista de herramientas para inyectar en Gemini
SILO_TOOLS = [search_patients, register_patient, validate_insurance, send_admission_alert]
