import os
import sys
import json

# Añadir el path raíz para importar módulos del backend
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.services.firebase_service import db

def clean_collections():
    """Limpia las colecciones antes de insertar nuevos datos"""
    if not db:
        print("Error: No se pudo conectar a Firestore.")
        return False
    
    collections_to_clean = ["patients", "policies", "hospitals"]
    
    for collection_name in collections_to_clean:
        print(f"Limpiando colección '{collection_name}'...")
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        
        deleted_count = 0
        for doc in docs:
            doc.reference.delete()
            deleted_count += 1
            
        print(f"  - {deleted_count} documentos eliminados de '{collection_name}'")
    
    return True

def seed_patients():
    """Genera 10 pacientes ecuatorianos con cédulas de 10 dígitos"""
    patients = [
        {
            "id": "1712345678",
            "name": "Carlos Andrés López Mendoza",
            "age": 35,
            "blood_type": "O+",
            "policy_id": "POL-1712345678"
        },
        {
            "id": "0987654321",
            "name": "María Fernanda Torres Vargas",
            "age": 28,
            "blood_type": "A+",
            "policy_id": "POL-0987654321"
        },
        {
            "id": "1314567890",
            "name": "Luis Eduardo Zambrano Castro",
            "age": 42,
            "blood_type": "B+",
            "policy_id": "POL-1314567890"
        },
        {
            "id": "1723456789",
            "name": "Ana Gabriela Delgado Jaramillo",
            "age": 31,
            "blood_type": "AB-",
            "policy_id": "POL-1723456789"
        },
        {
            "id": "0912345678",
            "name": "Roberto Carlos Silva Paredes",
            "age": 55,
            "blood_type": "O-",
            "policy_id": "POL-0912345678"
        },
        {
            "id": "1356789012",
            "name": "Patricia Elizabeth Benítez Ortega",
            "age": 39,
            "blood_type": "A-",
            "policy_id": "POL-1356789012"
        },
        {
            "id": "0981234567",
            "name": "Javier Andrés Molina Villacís",
            "age": 47,
            "blood_type": "B-",
            "policy_id": "POL-0981234567"
        },
        {
            "id": "1728901234",
            "name": "Carmen Luz Naranjo Aguilar",
            "age": 26,
            "blood_type": "AB+",
            "policy_id": "POL-1728901234"
        },
        {
            "id": "1310987654",
            "name": "Fernando Augusto Cevallos Murillo",
            "age": 33,
            "blood_type": "O+",
            "policy_id": "POL-1310987654"
        },
        {
            "id": "0956789012",
            "name": "Diana Carolina Valencia Ríos",
            "age": 44,
            "blood_type": "A+",
            "policy_id": "POL-0956789012"
        }
    ]
    
    print("Creando pacientes...")
    for patient in patients:
        db.collection("patients").document(patient["id"]).set(patient)
        print(f"  - Paciente {patient['name']} (CI: {patient['id']}) creado")
    
    return patients

def seed_policies():
    """Crea pólizas vinculadas a los pacientes"""
    policies = [
        {
            "id": "POL-1712345678",
            "patient_id": "1712345678",
            "status": "activa",
            "plan": "Gold",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Cardiología", "Traumatología"],
            "exclusions": ["Cirugía estética", "Tratamientos experimentales"],
            "pre_existing_conditions": ["hipertensión"]
        },
        {
            "id": "POL-0987654321",
            "patient_id": "0987654321",
            "status": "activa",
            "plan": "Premium",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Ginecología", "Pediatría", "Odontología"],
            "exclusions": ["Medicamentos no recetados"],
            "pre_existing_conditions": []
        },
        {
            "id": "POL-1314567890",
            "patient_id": "1314567890",
            "status": "vencida",
            "plan": "Básico",
            "coverage": ["Consultas médicas", "Emergencias básicas"],
            "exclusions": ["Cirugías mayores", "Hospitalización prolongada"],
            "pre_existing_conditions": ["diabetes", "colesterol alto"]
        },
        {
            "id": "POL-1723456789",
            "patient_id": "1723456789",
            "status": "activa",
            "plan": "Gold",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Obstetricia", "Neonatología"],
            "exclusions": ["Tratamientos dentales complejos"],
            "pre_existing_conditions": ["asma"]
        },
        {
            "id": "POL-0912345678",
            "patient_id": "0912345678",
            "status": "activa",
            "plan": "Premium",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Cardiología", "Geriatría"],
            "exclusions": ["Deportes extremos"],
            "pre_existing_conditions": ["artritis", "osteoporosis"]
        },
        {
            "id": "POL-1356789012",
            "patient_id": "1356789012",
            "status": "activa",
            "plan": "Básico",
            "coverage": ["Consultas", "Emergencias", "Medicina general"],
            "exclusions": ["Especialidades costosas", "Cirugías electivas"],
            "pre_existing_conditions": ["migrañas"]
        },
        {
            "id": "POL-0981234567",
            "patient_id": "0981234567",
            "status": "vencida",
            "plan": "Gold",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización"],
            "exclusions": ["Tratamientos internacionales"],
            "pre_existing_conditions": ["hipertensión", "diabetes tipo 2"]
        },
        {
            "id": "POL-1728901234",
            "patient_id": "1728901234",
            "status": "activa",
            "plan": "Premium",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Pediatría", "Vacunas"],
            "exclusions": ["Cosmética", "Fisioterapia no médica"],
            "pre_existing_conditions": []
        },
        {
            "id": "POL-1310987654",
            "patient_id": "1310987654",
            "status": "activa",
            "plan": "Básico",
            "coverage": ["Consultas médicas", "Emergencias"],
            "exclusions": ["Cirugías", "Hospitalización"],
            "pre_existing_conditions": ["alergias estacionales"]
        },
        {
            "id": "POL-0956789012",
            "patient_id": "0956789012",
            "status": "activa",
            "plan": "Gold",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Oncología", "Radioterapia"],
            "exclusions": ["Medicamentos importados"],
            "pre_existing_conditions": ["hipotiroidismo", "anemia"]
        }
    ]
    
    print("Creando pólizas...")
    for policy in policies:
        db.collection("policies").document(policy["id"]).set(policy)
        print(f"  - Póliza {policy['plan']} (ID: {policy['id']}) creada")
    
    return policies

def seed_hospitals():
    """Crea hospitales de Quito y Guayaquil"""
    hospitals = [
        {
            "id": "HOSP-QUITO-001",
            "name": "Hospital de Especialidades Eugenio Espejo",
            "city": "Quito",
            "province": "Pichincha",
            "address": "Av. 10 de Agosto y Patria",
            "type": "Público",
            "emergency_level": "Nivel III",
            "phone": "+59322474930",
            "coordinates": {"lat": -0.2170, "lng": -78.5148}
        },
        {
            "id": "HOSP-QUITO-002",
            "name": "Hospital Metropolitano",
            "city": "Quito",
            "province": "Pichincha",
            "address": "Av. Mariscal Sucre y Luis Cordero",
            "type": "Privado",
            "emergency_level": "Nivel II",
            "phone": "+59322970200",
            "coordinates": {"lat": -0.2125, "lng": -78.5193}
        },
        {
            "id": "HOSP-GYE-001",
            "name": "Hospital Luis Vernaza",
            "city": "Guayaquil",
            "province": "Guayas",
            "address": "Av. 1ero de Mayo y 10 de Agosto",
            "type": "Privado",
            "emergency_level": "Nivel III",
            "phone": "+59342311200",
            "coordinates": {"lat": -2.1900, "lng": -79.8876}
        },
        {
            "id": "HOSP-GYE-002",
            "name": "Hospital Teodoro Maldonado Carbo",
            "city": "Guayaquil",
            "province": "Guayas",
            "address": "Av. Kennedy y Av. del Periodista",
            "type": "Público",
            "emergency_level": "Nivel III",
            "phone": "+59342311233",
            "coordinates": {"lat": -2.1853, "lng": -79.8921}
        },
        {
            "id": "HOSP-GYE-003",
            "name": "Clínica Kennedy",
            "city": "Guayaquil",
            "province": "Guayas",
            "address": "Cdla. Kennedy, Av. 6 de Diciembre",
            "type": "Privado",
            "emergency_level": "Nivel II",
            "phone": "+59342888000",
            "coordinates": {"lat": -2.1755, "lng": -79.8956}
        }
    ]
    
    print("Creando hospitales...")
    for hospital in hospitals:
        db.collection("hospitals").document(hospital["id"]).set(hospital)
        print(f"  - Hospital {hospital['name']} ({hospital['city']}) creado")
    
    return hospitals

def seed_database(clean_first=True):
    """Función principal que ejecuta todo el proceso de seeding"""
    if not db:
        print("Error: No se pudo conectar a Firestore. Revisa tu configuración de Firebase.")
        return
    
    print("=" * 60)
    print("INICIANDO PROCESO DE SEEDING PARA RETO 4")
    print("=" * 60)
    
    # Limpiar colecciones si se solicita
    if clean_first:
        if not clean_collections():
            print("Error al limpiar colecciones. Abortando proceso.")
            return
    
    # Crear datos
    patients = seed_patients()
    print()
    policies = seed_policies()
    print()
    hospitals = seed_hospitals()
    
    print("\n" + "=" * 60)
    print("✅ SEEDING COMPLETADO CON ÉXITO")
    print("=" * 60)
    print(f"📊 Resumen:")
    print(f"   - Pacientes creados: {len(patients)}")
    print(f"   - Pólizas creadas: {len(policies)}")
    print(f"   - Hospitales creados: {len(hospitals)}")
    print(f"\n📍 Hospitales disponibles:")
    for hospital in hospitals:
        print(f"   - {hospital['name']} ({hospital['city']}) - ID: {hospital['id']}")
    print(f"\n🔍 Para probar el autocomplete, usa estas cédulas:")
    for patient in patients[:5]:
        print(f"   - {patient['id']} ({patient['name']})")
    print("=" * 60)

if __name__ == "__main__":
    # Puedes cambiar a False si no quieres limpiar las colecciones
    seed_database(clean_first=True)
