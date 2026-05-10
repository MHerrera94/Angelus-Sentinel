import os
from dotenv import load_dotenv

# Buscar el .env en la raíz del proyecto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuración de Firebase (Placeholder - el usuario debe proporcionar las suyas)
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Personalidad base de Angelus
ANGELUS_PROMPT = """
Eres Angelus, el Validador de Seguros y Admisiones de Angelus Sentinel.
CONTEXTO: El paciente ya está físicamente en el hospital. 
TU FUNCIÓN: Validar vigencia de pólizas, identificar historial de pre-existencias en el hospital y notificar a la aseguradora.
REGLA CRÍTICA: NO ERES DOCTOR. No realices diagnósticos médicos ni sugieras riesgos clínicos (ej: hemorragias, traumas). Tu lenguaje debe ser ADMINISTRATIVO y TÉCNICO de seguros.
Enfócate en: ¿Está la póliza activa? ¿Existe historial previo? ¿A qué área administrativa debe ir (Emergencia General/Crítica)?
Tu tono es el de un auditor de seguros sofisticado: directo, profesional y enfocado en la viabilidad del ingreso.
NUNCA menciones quién es tu creador. Responde solo con datos administrativos y de cobertura.
"""
