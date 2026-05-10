import requests
import json

def test_multicoat_webhook():
    url = "http://localhost:8000/webhook/emergency"
    
    # Datos de Santiago Guerrero (ISSFA + PRIVADO)
    payload = {
        "patient_id": "0933333333",
        "hospital_id": "HOSP-SENTINEL-01",
        "emergency_type": "Traumatismo craneal por accidente laboral",
        "operator_name": "Sistema de Emergencias 911"
    }
    
    print(f"🚀 Enviando Webhook de Multicobertura para Santiago Guerrero...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Respuesta de Angelus:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Error al conectar con el servidor: {e}")

if __name__ == "__main__":
    test_multicoat_webhook()
