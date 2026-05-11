import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from backend.config import load_dotenv

# Asegurar que las variables de entorno estén cargadas
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

firebase_app = None
db = None

def initialize_firebase():
    global firebase_app, db
    
    if not firebase_admin._apps:
        # Intentar cargar desde variable de entorno (JSON string)
        service_account_info = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        
        try:
            if service_account_info:
                # Parsear el string JSON
                info = json.loads(service_account_info)
                cred = credentials.Certificate(info)
            else:
                # Fallback a archivo físico si existe
                cred_path = os.path.join(os.path.dirname(__file__), "..", "..", "serviceAccountKey.json")
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                else:
                    print("ERROR: No se encontró configuración de Firebase (JSON o archivo)")
                    return None
            
            firebase_app = firebase_admin.initialize_app(cred)
            db = firestore.client(database_id="sentinel")
            print("Firebase inicializado correctamente en la base de datos 'sentinel'")
        except Exception as e:
            print(f"Error al inicializar Firebase: {e}")
            return None
    else:
        db = firestore.client(database_id="sentinel")
    
    return db

# Inicializar al importar si es posible
db = initialize_firebase()

def federated_search(name_query: str = None, ci_query: str = None):
    """
    Busca un paciente en las 6 bases de datos simuladas.
    Agrupa resultados por CI.
    """
    collections = [
        "db_hospital_publico", "db_hospital_privado", "db_clinica", 
        "db_seguro_iess", "db_seguro_privado", "db_salud_publica"
    ]
    
    results_by_ci = {}
    
    if not db:
        return results_by_ci

    for col_name in collections:
        col_ref = db.collection(col_name)
        docs = col_ref.stream()
        
        for doc in docs:
            data = doc.to_dict()
            p_name = data.get("name", "").lower()
            p_id = data.get("id", "")
            
            # Match por CI (prioritario) o por Nombre
            match = False
            if ci_query and ci_query == p_id:
                match = True
            elif name_query and name_query.lower() in p_name:
                match = True
                
            if match:
                if p_id not in results_by_ci:
                    results_by_ci[p_id] = {
                        "id": p_id,
                        "name": data.get("name"),
                        "sources": []
                    }
                # Añadir datos de esta fuente
                source_data = {"source": col_name, "data": data}
                results_by_ci[p_id]["sources"].append(source_data)
                
                # Consolidar datos para análisis
                if col_name in ["db_hospital_publico", "db_hospital_privado", "db_clinica"]:
                    results_by_ci[p_id]["clinical_history"] = data
                if col_name in ["db_seguro_iess", "db_seguro_privado"]:
                    results_by_ci[p_id]["insurance_policy"] = data
                    
    return list(results_by_ci.values())
