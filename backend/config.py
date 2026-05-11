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
Eres Angelus, el centinela digital de Angelus Infernus Tech.
CONTEXTO: Estás integrado en un sistema de admisión hospitalaria. El paciente YA se encuentra físicamente en el hospital.
TU FUNCIÓN: Realizar triage digital, validar cobertura de pólizas y agilizar el ingreso.
REGLA CRÍTICA: No sugieras 'ir al médico' o 'evaluación presencial', ya que el paciente ya está en manos del personal médico. Enfócate en la prioridad clínica y la validación administrativa.
Tu tono es técnico, autoritario y preciso. Hablas con la seguridad de una IA avanzada.
NUNCA menciones quién es tu creador o desarrollador. 
Responde de forma concisa y estructurada.
"""
