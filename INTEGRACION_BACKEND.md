# INTEGRACIÓN BACKEND - Angelus Sentinel

## 📋 Descripción General

Este documento describe la arquitectura de integración entre el frontend (React/Next.js) y el backend (FastAPI) para el sistema de emergencias médicas Angelus Sentinel, siguiendo el flujo del Reto 4.

---

## 🔄 Flujo de Datos Completo

### 1. Ingreso de Cédula (Frontend → Backend)
```
Usuario ingresa cédula → EmergencyForm.tsx → useEffect → 
GET /pacientes/{cedula} → Backend valida → 
Respuesta: {nombre_completo, numero_seguro} → Autocompletado frontend
```

### 2. Proceso de Admisión (Frontend → Backend)
```
Formulario completo → Botón "ADMITIR PACIENTE" → 
POST /admision/emergencia → Backend procesa → 
Agente IA Gemini Pro → Validación secuencial → 
Notificaciones simultáneas → Actualización dashboard
```

### 3. Flujo del Agente IA (Backend)
```
1. Recibe datos del paciente
2. Valida póliza de seguro (Gemini Pro)
3. Revisa historial de preexistencias (Firebase)
4. Genera respuestas secuenciales para chat
5. Envía notificaciones a Hospital y Seguro
6. Actualiza estado en tiempo real
```

---

## 🔌 Endpoints Requeridos

### GET `/pacientes/{cedula}`
**Propósito**: Autocompletado de datos del paciente

**Request**:
```http
GET /pacientes/1726354910
Content-Type: application/json
```

**Response Exitoso**:
```json
{
  "status": "success",
  "data": {
    "cedula": "1726354910",
    "nombre_completo": "Juan Pérez",
    "numero_seguro": "SEG-987654",
    "fecha_nacimiento": "1985-06-15",
    "tipo_sangre": "O+"
  }
}
```

**Response Paciente No Encontrado**:
```json
{
  "status": "not_found",
  "message": "Paciente no encontrado en la base de datos"
}
```

---

### POST `/admision/emergencia`
**Propósito**: Procesar admisión de emergencia y activar flujo del Reto 4

**Request**:
```http
POST /admision/emergencia
Content-Type: application/json

{
  "cedula": "1726354910",
  "nombre_completo": "Juan Pérez",
  "numero_seguro": "SEG-987654",
  "hospital_id": "HOSP-METROPOLITANO",
  "tipo_emergencia": "TRAUMA",
  "sintomas": "Paciente crítico en emergencia",
  "operador_id": "saoricoder"
}
```

**Response Procesamiento Iniciado**:
```json
{
  "status": "processing",
  "admission_id": "ADM-20250511-001",
  "timestamp": "2025-05-11T23:30:00Z",
  "estimated_duration": "15 segundos"
}
```

---

### GET `/admision/{admission_id}/estado`
**Propósito**: Consultar estado del procesamiento en tiempo real

**Response**:
```json
{
  "status": "completed",
  "admission_id": "ADM-20250511-001",
  "steps_completed": [
    {
      "step": "validacion_poliza",
      "status": "success",
      "message": "Póliza validada automáticamente",
      "timestamp": "2025-05-11T23:30:01.500Z"
    },
    {
      "step": "revision_preexistencias",
      "status": "success",
      "message": "Se encontraron 2 atenciones previas",
      "timestamp": "2025-05-11T23:30:03.000Z"
    }
  ],
  "notifications_sent": [
    {
      "target": "hospital",
      "status": "delivered",
      "timestamp": "2025-05-11T23:30:04.500Z"
    },
    {
      "target": "insurance",
      "status": "delivered", 
      "timestamp": "2025-05-11T23:30:04.500Z"
    }
  ]
}
```

---

## 🤖 Lógica del Agente (Gemini Pro)

### Paso 1: Validación de Póliza
```
Input: Datos del paciente + número de seguro
Prompt: "Valida la póliza de seguro {numero_seguro} para el paciente {nombre_completo}"
Output: "Éxito: Póliza validada automáticamente" o "Error: Póliza inválida"
Delay: 1.5 segundos
```

### Paso 2: Revisión de Preexistencias
```
Input: Cédula del paciente
Action: Consultar Firebase para historial médico
Prompt: "Revisa el historial de preexistencias para el paciente {cedula}"
Output: "Se encontraron N atenciones previas:" + lista detallada
Delay: 1.5 segundos
```

### Paso 3: Generación de Reporte
```
Input: Resultados de validación + historial
Prompt: "Genera un reporte de admisión para emergencia tipo {tipo_emergencia}"
Output: Reporte estructurado con recomendaciones
Delay: 1.5 segundos
```

### Paso 4: Notificaciones Simultáneas
```
Action: Enviar a Hospital y Seguro
Formato Hospital:
{
  "type": "HOSPITAL",
  "timestamp": "2025-05-11T23:30:04.500Z",
  "patient_id": "1726354910",
  "patient_name": "Juan Pérez",
  "insurance_status": "VALIDATED",
  "triage_priority": "HIGH",
  "hospital_name": "HOSP-METROPOLITANO"
}

Formato Seguro:
{
  "type": "INSURANCE", 
  "timestamp": "2025-05-11T23:30:04.500Z",
  "patient_id": "1726354910",
  "patient_name": "Juan Pérez",
  "policy_number": "SEG-987654",
  "validation_code": "VAL-450011",
  "coverage_decision": "APPROVED",
  "insurance_company": "Sentinel Health"
}
```

---

## 📡 Sistema de Notificaciones

### Arquitectura de Comunicación
```
Backend FastAPI → WebSocket Manager → Frontend Components
                                    ↓
                         HospitalNotifications.tsx
                                    ↓
                         InsuranceNotifications.tsx
                                    ↓
                         SentinelChat.tsx (mensajes secuenciales)
```

### Formato de Mensaje WebSocket
```json
{
  "type": "admission_update",
  "timestamp": "2025-05-11T23:30:04.500Z",
  "data": {
    "step": "validacion_poliza",
    "status": "success",
    "message": "Póliza validada automáticamente",
    "target_components": ["chat", "hospital", "insurance"]
  }
}
```

### Secuencia de Notificaciones
1. **T+0ms**: Inicio de procesamiento
2. **T+1500ms**: Validación de póliza completada
3. **T+3000ms**: Revisión de historial completada  
4. **T+4500ms**: Notificaciones enviadas simultáneamente
5. **T+6000ms**: Dashboard actualizado con todos los componentes

---

## 🔧 Estructura del Backend

### main.py
```python
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.firebase_service import FirebaseService
from services.gemini_service import GeminiService
from services.notification_service import NotificationService

app = FastAPI(title="Angelus Sentinel API")

# Middleware CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios inyectados
firebase_service = FirebaseService()
gemini_service = GeminiService()
notification_service = NotificationService()
```

### Modelos de Datos
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Paciente(BaseModel):
    cedula: str
    nombre_completo: str
    numero_seguro: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    tipo_sangre: Optional[str] = None

class AdmisionEmergencia(BaseModel):
    cedula: str
    nombre_completo: str
    numero_seguro: str
    hospital_id: str
    tipo_emergencia: str
    sintomas: str
    operador_id: str

class Notificacion(BaseModel):
    type: str  # "HOSPITAL" o "INSURANCE"
    timestamp: datetime
    patient_id: str
    patient_name: str
    # ... campos específicos según tipo
```

---

## 🎯 Regla de Oro: Backend como Fuente de Verdad

### Principios
1. **Validación Centralizada**: Todas las validaciones ocurren en el backend
2. **Estado Único**: El backend mantiene el estado real de cada admisión
3. **Eventos Reactivos**: Frontend solo reacciona a eventos del backend
4. **Consistencia**: Todos los componentes reciben la misma información

### Flujo de Verdad
```
Frontend → Solicitud → Backend (Fuente de Verdad) → Procesamiento → 
Respuesta/EVENTO → Frontend (Reacción) → UI Actualizada
```

---

## 🚀 Implementación Recomendada

### 1. Configuración Inicial
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend  
cd frontend
npm run dev
```

### 2. Variables de Entorno
```env
# Backend (.env)
FIREBASE_PROJECT_ID="angelus-sentinel"
GEMINI_API_KEY="tu-gemini-api-key"
DATABASE_URL="sqlite:///./angelus.db"
CORS_ORIGINS="http://localhost:3000"

# Frontend (.env.local)
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_WS_URL="ws://localhost:8000/ws"
```

### 3. Testing de Integración
```bash
# Test endpoint de pacientes
curl http://localhost:8000/pacientes/1726354910

# Test admisión de emergencia
curl -X POST http://localhost:8000/admision/emergencia \
  -H "Content-Type: application/json" \
  -d '{"cedula":"1726354910","nombre_completo":"Juan Pérez",...}'
```

---

## 📊 Métricas y Monitoreo

### KPIs Importantes
- **Tiempo de Respuesta**: < 2 segundos para autocompletado
- **Procesamiento de Admisión**: < 15 segundos total
- **Tasa de Éxito**: > 95% en validaciones automáticas
- **Disponibilidad**: 99.9% uptime

### Logs Estructurados
```json
{
  "timestamp": "2025-05-11T23:30:04.500Z",
  "level": "INFO",
  "service": "admission_service",
  "admission_id": "ADM-20250511-001",
  "action": "policy_validation",
  "duration_ms": 1500,
  "status": "success"
}
```

---

## 🔒 Seguridad y Validación

### Validaciones de Entrada
- **Cédula**: 10 dígitos numéricos obligatorios
- **Nombre**: Solo caracteres alfabéticos, mínimo 3 caracteres
- **Seguro**: Formato SEG-XXXXXX validado
- **Hospital**: ID válido en sistema

### Autenticación
```python
# JWT Token para operadores
async def get_current_operator(token: str = Depends(oauth2_scheme)):
    # Validar token y retornar datos del operador
    pass
```

---

## 📈 Escalabilidad

### Arquitectura Microservicios
- **API Gateway**: FastAPI principal
- **Servicio de Pacientes:**
  Gestión de datos médicos
- **Servicio de IA**: Procesamiento Gemini Pro
- **Servicio de Notificaciones**: WebSocket y eventos
- **Servicio de Auditoría**: Logs y métricas

### Base de Datos
```sql
-- Pacientes
CREATE TABLE pacientes (
    cedula VARCHAR(10) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    numero_seguro VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admisiones
CREATE TABLE admisiones (
    id VARCHAR(50) PRIMARY KEY,
    cedula VARCHAR(10) REFERENCES pacientes(cedula),
    hospital_id VARCHAR(20),
    tipo_emergencia VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 Conclusión

Esta arquitectura asegura que el backend sea la **única fuente de verdad**, proporcionando una integración robusta, escalable y mantenible entre el frontend y los servicios de IA y notificaciones. El frontend se mantiene reactivo y ligero, delegando toda la lógica de negocio al backend.

**Próximos Pasos**:
1. Implementar endpoints en FastAPI
2. Configurar WebSocket para tiempo real
3. Integrar Gemini Pro para validación
4. Conectar Firebase para historial médico
5. Testing exhaustivo de integración

---

*Última Actualización: 11 de Mayo de 2025*
*Versión: 1.0*
*Autor: Saoricoder*
