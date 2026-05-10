# 🛡️ Angelus Sentinel: Centro de Monitoreo de Emergencias

**Angelus Sentinel** es una solución de vanguardia diseñada para transformar la admisión hospitalaria en un proceso autónomo, inteligente y humano. Este proyecto ha sido desarrollado para el **[Hack-i-athon 2026](https://hackiathon.dev/): Inteligencia Artificial Generativa**, enfocándose en la optimización de tiempos críticos mediante agentes inteligentes.

---

## 🏛️ Sección 1: Información del Proyecto y Visión

### 👥 Participantes
*   **Angelus Infernus** (@AngelusInfernus): Arquitectura de Sistemas y Estrategia de IA.
*   **Saoricoder** (@Saoricoder): Desarrollo Fullstack y Diseño de Experiencia de Usuario (UX/UI).

---

### 🌟 Sobre el Hack-i-athon 2026
El **[Hack-i-athon 2026](https://hackiathon.dev/): Inteligencia Artificial Generativa** es la tercera edición de la competencia de IA más grande del Ecuador. Organizado por **Viamatica**, **IT Ahora** y **Citytech**, con **Aseguradora del Sur** como Líder de Innovación.

Este proyecto, **Angelus Sentinel**, nace como una respuesta directa a la visión del evento, utilizando IA Generativa con arquitectura de agentes (Function Calling) para humanizar y agilizar la atención médica de emergencia.

---

### 🏆 El Desafío: Tema 4 - Sistema de Alerta Temprana de Ingresos a Emergencias
**Requerimiento Original (Tema 4):**
> "4. Sistema de Alerta Temprana de Ingresos a Emergencias 
> Descripción: Un webhook que se activa cuando un asegurado ingresa a la emergencia del hospital. Un agente revisa instantáneamente la validez de la póliza, el historial de pre-existencias y envía una notificación al departamento de admisiones del hospital y al gestor de casos del seguro simultáneamente."

**Cómo lo Resolvimos (Nuestra Solución):**
Para cumplir y superar esta premisa, hemos construido a **Angelus**, un **Agente Autónomo** con "Manos y Dedos" (Function Calling) que actúa como un centinela digital capaz de operar sobre ecosistemas de datos federados. El sistema implementa el flujo solicitado con arquitectura de "Cero Fricción":
1.  **Orquestación Autónoma:** Angelus no es un simple bot conversacional; es un agente orquestador que usa herramientas especializadas (`search_patients`, `register_patient`, `validate_insurance`, `send_admission_alert`) para tomar decisiones complejas sin requerir promteos manuales paso a paso.
2.  **Búsqueda Federada B2B:** Emulamos múltiples silos de datos de diferentes entidades (IESS, MSP, Clínicas Privadas, Hospitales Públicos) para construir un perfil holístico del paciente.
3.  **Activación por Webhook:** El sistema puede dispararse automáticamente cuando un hospital registra un ingreso a través de sistemas pre-existentes, sin interacción humana inicial.
4.  **Triage Clínico-Administrativo:** Usando **Gemini Flash Lite 3.1**, el agente analiza los síntomas y cruza la información con la póliza del paciente en milisegundos.
5.  **Notificación Simultánea:** Envía alertas instantáneas y estructuradas tanto al canal clínico del hospital como al canal administrativo del seguro.

---

## ⚙️ Sección 2: Tecnologías y Configuración del Entorno

### 🚀 Stack Tecnológico
*   **Backend:** FastAPI (Python 3.10+) - Alta velocidad y validación de tipos asíncrona.
*   **IA Cerebro:** Google Gemini 3.1 Flash Lite (Generative AI SDK con soporte Function Calling).
*   **Base de Datos:** Firebase Firestore (NoSQL) para persistencia en tiempo real y federación de silos.
*   **Frontend:** Next.js 16 (App Router) + React 19 + TypeScript.
*   **Estilos:** Tailwind CSS con estética *Glassmorphism* y Dark Mode.
*   **Iconografía:** Lucide React.

### 🛠️ Configuración e Instalación

#### 1. Requisitos Previos
*   Python 3.10 o superior instalado.
*   Node.js 18 o superior instalado.
*   Cuenta de Google Cloud / Firebase (con API Key de Gemini y JSON de credenciales de servicio).

#### 2. Configuración General
1.  Configura tu archivo `.env` en la raíz del proyecto:
    ```env
    GEMINI_API_KEY=tu_api_key_aqui
    FIREBASE_SERVICE_ACCOUNT_JSON=ruta/a/tu/firebase-key.json
    ```
2. Instala las dependencias del Backend (dentro de la carpeta `/backend` o entorno virtual):
    ```bash
    pip install fastapi uvicorn google-generativeai firebase-admin python-dotenv pydantic
    ```
3. Instala las dependencias del Frontend (dentro de la carpeta `/frontend`):
    ```bash
    npm install
    ```

#### 3. Ejecución del Sistema (Método Recomendado)
Hemos creado un script lanzador para simplificar la inicialización del ecosistema:

1. Ubícate en la raíz del proyecto.
2. Haz doble clic en el archivo **`start_sentinel.bat`** (En Windows).
3. Se abrirán automáticamente dos ventanas de consola manejando el Backend (FastAPI en puerto 8000) y el Frontend (Next.js en puerto 3000).

*Nota: Si prefieres iniciarlo manualmente, puedes correr `python -m uvicorn backend.main:app --reload --port 8000` y `npm run dev` en sus respectivas carpetas.*

---

### 📡 Uso del Dashboard y Simulador (Tema 4)
Una vez en el dashboard (`http://localhost:3000`), cuentas con dos pestañas principales en el cuadrante superior derecho:

1. **Formulario Manual:** Para probar el flujo conversacional y la atención a pacientes que llegan sin registro previo o interactuar directamente con la IA para completar registros.
2. **Simular Webhook (B2B):** Pestaña principal. Presiona el botón amarillo para inyectar un payload aleatorio desde un sistema externo. Angelus interceptará el webhook y ejecutará el Function Calling iterativo para validar pólizas, analizar historiales y notificar de forma totalmente automatizada.

---
*Angelus Sentinel - Protegiendo lo que importa, cuando más importa.*
