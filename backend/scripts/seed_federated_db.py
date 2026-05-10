import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.firebase_service import db

def seed_database():
    if not db:
        print("Error: No se pudo conectar a Firebase.")
        return
        
    print("Iniciando carga masiva de datos federados simulados...")

    # PACIENTES UNIVERSALES (En todas las bases de datos)
    universal_patients = [
        {"id": "0922222222", "name": "Elena Narváez", "age": 32},
        {"id": "1733333333", "name": "Roberto Gómez", "age": 50}
    ]

    # 1. db_hospital_publico
    public_hosp = db.collection("db_hospital_publico")
    data_1 = [
        {"id": "0912345678", "name": "Juan Pérez", "age": 45, "blood_type": "O+", "history": "Asma leve"},
        {"id": "1234567890", "name": "Ana López", "age": 60, "blood_type": "A-", "history": "Diabetes Tipo 2"},
        {"id": "0922222222", "name": "Elena Narváez", "history": "Apendicectomía 2020"},
        {"id": "1733333333", "name": "Roberto Gómez", "history": "Fractura de fémur"},
        {"id": "0144444444", "name": "Sofía Castro", "age": 25, "history": "Sana"},
        {"id": "0855555555", "name": "Mateo Villalba", "age": 19, "history": "Alergia polen"},
        {"id": "1066666666", "name": "Lucía Méndez", "age": 41, "history": "Hipotiroidismo"}
    ]
    for d in data_1: public_hosp.document(d["id"]).set(d)

    # 2. db_hospital_privado
    private_hosp = db.collection("db_hospital_privado")
    data_2 = [
        {"id": "1111111111", "name": "Carlos Ruiz", "age": 35, "vip_status": True, "history": "Hipertensión"},
        {"id": "0922222222", "name": "Elena Narváez", "vip_status": False, "history": "Checkup anual OK"},
        {"id": "1733333333", "name": "Roberto Gómez", "vip_status": True, "history": "Cirugía ocular"},
        {"id": "0144444444", "name": "Sofía Castro", "history": "Gripe estacional"},
        {"id": "0855555555", "name": "Mateo Villalba", "history": "Lesión deportiva"},
        {"id": "1066666666", "name": "Lucía Méndez", "history": "Migrañas"}
    ]
    for d in data_2: private_hosp.document(d["id"]).set(d)

    # 3. db_clinica
    clinica = db.collection("db_clinica")
    data_3 = [
        {"id": "0999999999", "name": "María García", "age": 28, "allergies": ["Penicilina"]},
        {"id": "0922222222", "name": "Elena Narváez", "allergies": ["Nueces"]},
        {"id": "1733333333", "name": "Roberto Gómez", "allergies": ["Aspirina"]},
        {"id": "0144444444", "name": "Sofía Castro", "allergies": ["Lactosa"]},
        {"id": "0855555555", "name": "Mateo Villalba", "allergies": ["Ninguna"]},
        {"id": "1066666666", "name": "Lucía Méndez", "allergies": ["Polvo"]}
    ]
    for d in data_3: clinica.document(d["id"]).set(d)

    # 4. db_seguro_iess
    iess = db.collection("db_seguro_iess")
    data_4 = [
        {"id": "0999999999", "name": "María García", "status": "Activo", "employer": "Tech Corp"},
        {"id": "1234567890", "name": "Ana López", "status": "Jubilado", "employer": "Estado"},
        {"id": "0922222222", "name": "Elena Narváez", "status": "Activo", "employer": "Banco Central"},
        {"id": "1733333333", "name": "Roberto Gómez", "status": "Activo", "employer": "PetroEcuador"},
        {"id": "0144444444", "name": "Sofía Castro", "status": "Cesante", "employer": "N/A"},
        {"id": "0855555555", "name": "Mateo Villalba", "status": "Dependiente", "employer": "Padres"},
        {"id": "1066666666", "name": "Lucía Méndez", "status": "Activo", "employer": "Municipio"}
    ]
    for d in data_4: iess.document(d["id"]).set(d)

    # 5. db_seguro_privado
    priv_ins = db.collection("db_seguro_privado")
    data_5 = [
        {"id": "1712345678", "name": "Juan Pérez", "policy_type": "Estudiantil", "status": "Activo"},
        {"id": "1111111111", "name": "Carlos Ruiz", "policy_type": "Premium Elite", "status": "Activo"},
        {"id": "0922222222", "name": "Elena Narváez", "policy_type": "Global Care", "status": "Activo", "limit": 100000},
        {"id": "1733333333", "name": "Roberto Gómez", "policy_type": "Platinum", "status": "Inactivo", "reason": "Falta de pago"},
        {"id": "0144444444", "name": "Sofía Castro", "policy_type": "Básico", "status": "Activo"},
        {"id": "0855555555", "name": "Mateo Villalba", "policy_type": "Junior", "status": "Activo"},
        {"id": "1066666666", "name": "Lucía Méndez", "policy_type": "Familiar", "status": "Activo"}
    ]
    for d in data_5: priv_ins.document(d["id"]).set(d)

    # 6. db_salud_publica
    msp = db.collection("db_salud_publica")
    data_6 = [
        {"id": "0912345678", "name": "Juan Pérez", "vaccines": ["COVID-19", "Influenza"]},
        {"id": "0922222222", "name": "Elena Narváez", "vaccines": ["Hepatitis B", "Fiebre Amarilla"]},
        {"id": "1733333333", "name": "Roberto Gómez", "vaccines": ["Refuerzo COVID"]},
        {"id": "0144444444", "name": "Sofía Castro", "vaccines": ["Completo"]},
        {"id": "0855555555", "name": "Mateo Villalba", "vaccines": ["Salk", "Sabin"]},
        {"id": "1066666666", "name": "Lucía Méndez", "vaccines": ["Influenza"]}
    ]
    for d in data_6: msp.document(d["id"]).set(d)

    # 7. db_sentinel_hospital (Local)
    sentinel = db.collection("db_sentinel_hospital")
    data_7 = [
        {"id": "0912345678", "name": "Juan Pérez", "last_visit": "2024-01-15", "pre_existing_conditions": ["Asma"]},
        {"id": "1234567890", "name": "Ana López", "last_visit": "2023-11-20", "pre_existing_conditions": ["Diabetes"]},
        {"id": "0922222222", "name": "Elena Narváez", "last_visit": "2024-03-10", "pre_existing_conditions": ["Alergia Alimentaria"]},
        {"id": "1733333333", "name": "Roberto Gómez", "last_visit": "2024-02-25", "pre_existing_conditions": ["Glaucoma"]},
        {"id": "0144444444", "name": "Sofía Castro", "last_visit": "2023-12-05", "pre_existing_conditions": []},
        {"id": "0855555555", "name": "Mateo Villalba", "last_visit": "2024-04-01", "pre_existing_conditions": ["Rinitis"]},
        {"id": "1066666666", "name": "Lucía Méndez", "last_visit": "2024-01-30", "pre_existing_conditions": ["Migraña Crónica"]}
    ]
    for d in data_7: sentinel.document(d["id"]).set(d)

    print("Carga masiva completada. 2 pacientes universales y 3 nuevos en cada silo.")

if __name__ == "__main__":
    seed_database()
