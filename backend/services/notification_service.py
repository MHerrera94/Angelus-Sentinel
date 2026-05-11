import json
from datetime import datetime

class NotificationService:
    def __init__(self):
        # Aquí se podrían configurar webhooks reales de Discord, Slack, etc.
        self.logs = []

    async def notify_all(self, alert_data: dict, federated_data: dict = None):
        """
        Simula el envío de notificaciones simultáneas al hospital y a la aseguradora.
        """
        timestamp = datetime.now().isoformat()
        analysis = alert_data.get('analysis', {})
        decision = analysis.get('decision', 'REVISIÓN')
        triage = analysis.get('triage_priority', 'NO ESPECIFICADO')
        patient = alert_data.get('patient_name', 'Paciente')
        ci = alert_data.get('patient_id', 'N/A')

        # Extraer datos médicos (simulado)
        medical_history = federated_data.get('clinical_history', {}) if federated_data else {}
        insurance_data = federated_data.get('insurance_policy', {}) if federated_data else {}

        # Notificación 1: Hospital (Foco en Admisión y Triage)
        hosp_notif = {
            "timestamp": timestamp,
            "target": "Admisiones Hospital Sentinel",
            "message": f"Nueva Admisión: {patient} ({ci}). Prioridad: {triage}.",
            "type": "HOSPITAL",
            "status": "ENVIADO",
            "payload": {
                "admision_id": f"ADM-{datetime.now().strftime('%y%m%d%H%M')}",
                "paciente": patient,
                "cedula": ci,
                "motivo_ingreso": alert_data.get('emergency_type', ''),
                "historial_interno": medical_history.get('pre_existing_conditions', []),
                "triage_priority": triage,
                "triage_color": analysis.get('triage_color', '#f43f5e'),
                "area_destino": "Emergencia / Shock Room" if triage == "ADMIN_ALTA" else "Emergencia General"
            }
        }
        
        # Notificación 2: Aseguradora (Foco en Cobertura y Póliza)
        policies = federated_data.get('insurance_policies', []) if federated_data else []
        
        # Formatear lista de pólizas para el log
        if policies:
            poliza_info = {
                "id": f"{len(policies)} Pólizas Detectadas",
                "detalles": [f"{p['type']}: {p['plan']} ({p['status']})" for p in policies],
                "vigencia": "MULTICOBERTURA" if len(policies) > 1 else policies[0]['status']
            }
        else:
            poliza_info = {"id": "SIN SEGURO", "vigencia": "INEXISTENTE"}

        insu_notif = {
            "timestamp": timestamp,
            "target": "Gestoría de Cobertura (Seguro)",
            "message": f"Validación de Póliza: {patient}. Estado: {decision}.",
            "type": "INSURANCE",
            "status": "AUTORIZADO" if decision == "APROBADO" else "EN REVISIÓN",
            "payload": {
                "decision": decision,
                "insurance_status": poliza_info,
                "asegurado": patient,
                "symptoms": alert_data.get('emergency_type', 'Análisis en curso'),
                "preexistencias_relevantes": medical_history.get('pre_existing_conditions', []),
                "monto_estimado": "Sujeto a auditoría",
                "gestor_asignado": "Angelus Sentinel AI"
            }
        }

        # Guardar en logs y limitar tamaño
        self.logs.insert(0, hosp_notif)
        self.logs.insert(0, insu_notif)
        self.logs = self.logs[:50] 
        
        print(f"📡 [FEDERADO] Notificaciones diferenciadas enviadas para {patient}")
        return [hosp_notif, insu_notif]

notification_service = NotificationService()

