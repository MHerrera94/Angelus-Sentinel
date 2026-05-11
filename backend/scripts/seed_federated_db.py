import sys
import os

# Asegurar que el backend esté en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.firebase_service import db

def seed_database():
    if not db:
        print("Error: No se pudo conectar a Firebase.")
        return
        
    print("Iniciando carga de datos federados simulados...")

    # 1. db_hospital_publico
    public_hospital_ref = db.collection("db_hospital_publico")
    public_hospital_data = [
        {"id": "0912345678", "name": "Juan Pérez", "age": 45, "blood_type": "O+", "history": "Asma leve"},
        {"id": "1234567890", "name": "Ana López", "age": 60, "blood_type": "A-", "history": "Diabetes Tipo 2"}
    ]
    for d in public_hospital_data:
        public_hospital_ref.document(d["id"]).set(d)

    # 2. db_hospital_privado
    private_hospital_ref = db.collection("db_hospital_privado")
    private_hospital_data = [
        {"id": "1111111111", "name": "Carlos Ruiz", "age": 35, "vip_status": True, "history": "Hipertensión controlada"},
    ]
    for d in private_hospital_data:
        private_hospital_ref.document(d["id"]).set(d)

    # 3. db_clinica
    clinica_ref = db.collection("db_clinica")
    clinica_data = [
        {"id": "0999999999", "name": "María García", "age": 28, "allergies": ["Penicilina"]},
    ]
    for d in clinica_data:
        clinica_ref.document(d["id"]).set(d)

    # 4. db_seguro_iess
    iess_ref = db.collection("db_seguro_iess")
    iess_data = [
        {"id": "0999999999", "name": "María García", "status": "Activo", "employer": "Tech Corp S.A."},
        {"id": "1234567890", "name": "Ana López", "status": "Jubilado", "employer": "Estado"}
    ]
    for d in iess_data:
        iess_ref.document(d["id"]).set(d)

    # 5. db_seguro_privado
    seguro_privado_ref = db.collection("db_seguro_privado")
    seguro_privado_data = [
        {"id": "1712345678", "name": "Juan Pérez", "age": 22, "policy_type": "Estudiantil", "status": "Activo"}, # Diferente Juan Pérez
        {"id": "1111111111", "name": "Carlos Ruiz", "policy_type": "Premium Elite", "status": "Activo", "coverage_limit": 50000}
    ]
    for d in seguro_privado_data:
        seguro_privado_ref.document(d["id"]).set(d)

    # 6. db_salud_publica
    msp_ref = db.collection("db_salud_publica")
    msp_data = [
        {"id": "0912345678", "name": "Juan Pérez", "vaccines": ["COVID-19", "Influenza"]},
    ]
    for d in msp_data:
        msp_ref.document(d["id"]).set(d)

    print("Carga de datos simulados completada con éxito.")

if __name__ == "__main__":
    seed_database()
