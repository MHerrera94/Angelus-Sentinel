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
        {"id": "0999999999", "name": "María García", "status": "Activo", "employer": "Tech Corp", "plan": "Seguro General Obligatorio"},
        {"id": "1234567890", "name": "Ana López", "status": "Jubilado", "employer": "Estado", "plan": "Seguro de Pensiones"},
        {"id": "0922222222", "name": "Elena Narváez", "status": "Activo", "employer": "Banco Central", "plan": "Seguro General Obligatorio"},
        {"id": "1733333333", "name": "Roberto Gómez", "status": "Activo", "employer": "PetroEcuador", "plan": "Seguro General Obligatorio"},
        {"id": "1066666666", "name": "Lucía Méndez", "status": "Activo", "employer": "Municipio", "plan": "Seguro General Obligatorio"}
    ]
    for d in data_4: iess.document(d["id"]).set(d)

    # 4b. db_seguro_issfa (Fuerzas Armadas)
    issfa = db.collection("db_seguro_issfa")
    data_issfa = [
        {"id": "0933333333", "name": "Santiago Guerrero", "status": "Activo", "rank": "General", "plan": "Servicio Activo"},
        {"id": "1111111111", "name": "Carlos Ruiz", "status": "Activo", "rank": "Coronel (R)", "plan": "Servicio Pasivo"}
    ]
    for d in data_issfa: issfa.document(d["id"]).set(d)

    # 4c. db_seguro_isspol (Policía)
    isspol = db.collection("db_seguro_isspol")
    data_isspol = [
        {"id": "0944444444", "name": "Ricardo Mendoza", "status": "Activo", "rank": "Sargento", "plan": "Servicio Activo"}
    ]
    for d in data_isspol: isspol.document(d["id"]).set(d)

    # 5. db_seguro_privado
    priv_ins = db.collection("db_seguro_privado")
    data_5 = [
        {"id": "1111111111", "name": "Carlos Ruiz", "plan": "BMI Elite Internacional", "status": "Activo"},
        {"id": "0922222222", "name": "Elena Narváez", "plan": "Saludsa Ideal 500 (Familiar)", "status": "Activo", "limit": 100000},
        {"id": "0933333333", "name": "Santiago Guerrero", "plan": "Humana Global (Corporativo)", "status": "Activo"},
        {"id": "1733333333", "name": "Roberto Gómez", "plan": "Aseguradora del Sur - Plan Vive", "status": "Inactivo", "reason": "Falta de pago"},
        {"id": "0144444444", "name": "Sofía Castro", "plan": "Aseguradora del Sur - Plan Protege", "status": "Activo"},
        {"id": "0855555555", "name": "Mateo Villalba", "plan": "Aseguradora del Sur - Plan Salva", "status": "Activo"},
        {"id": "1066666666", "name": "Lucía Méndez", "plan": "Saludsa Pool (Individual)", "status": "Activo"}
    ]
    for d in data_5: priv_ins.document(d["id"]).set(d)

    # 6. db_salud_publica
    msp = db.collection("db_salud_publica")
    data_6 = [
        {"id": "0933333333", "name": "Santiago Guerrero", "vaccines": ["Fiebre Amarilla", "Tétanos"]},
        {"id": "0944444444", "name": "Ricardo Mendoza", "vaccines": ["COVID-19"]}
    ]
    for d in data_6: msp.document(d["id"]).set(d)

    # 7. db_sentinel_hospital (Local)
    sentinel = db.collection("db_sentinel_hospital")
    data_7 = [
        {"id": "0933333333", "name": "Santiago Guerrero", "last_visit": "2024-05-01", "pre_existing_conditions": ["Hipertensión"]},
        {"id": "0944444444", "name": "Ricardo Mendoza", "last_visit": "2024-02-15", "pre_existing_conditions": []}
    ]
    for d in data_7: sentinel.document(d["id"]).set(d)

    print("Carga masiva completada. Casos de Multicobertura (ISSFA/ISSPOL + Privado) añadidos.")

if __name__ == "__main__":
    seed_database()
