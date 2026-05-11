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

        # Notificación 1: Hospital (Payload Clínico)
        hosp_notif = {
            "timestamp": timestamp,
            "target": "Departamento de Urgencias (Hospital)",
            "message": f"Alerta Clínica: Paciente {patient} ({ci}) ingresado con triage {triage}.",
            "type": "HOSPITAL",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": patient,
                "ci": ci,
                "triage_priority": triage,
                "symptoms": alert_data.get('emergency_type', ''),
                "clinical_history": medical_history,
                "ai_recommendation": analysis.get('reasoning', '')
            }
        }
        
        # Notificación 2: Aseguradora (Payload Administrativo)
        insu_notif = {
            "timestamp": timestamp,
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": f"Validación de Cobertura: Paciente {patient} ({ci}). Estado de autorización: {decision}.",
            "type": "INSURANCE",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": patient,
                "ci": ci,
                "insurance_status": insurance_data,
                "triage_priority": triage,
                "decision": decision
            }
        }

        self.logs.insert(0, hosp_notif)
        self.logs.insert(0, insu_notif)
        
        print(f"📡 [SIMULTÁNEO] Notificaciones enviadas para {patient}")
        return [hosp_notif, insu_notif]

notification_service = NotificationService()

