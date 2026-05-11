# 🛡️ Angelus Sentinel: Centro de Monitoreo de Emergencias

**Angelus Sentinel** es una solución de vanguardia diseñada para transformar la admisión hospitalaria en un proceso autónomo, inteligente y humano. Este proyecto ha sido desarrollado para el **[Hack-i-athon 2026](https://hackiathon.dev/): Inteligencia Artificial Generativa**, enfocándose en la optimización de tiempos críticos mediante agentes inteligentes.

---

## 🏛️ Sección 1: Información del Proyecto y Visión

### 👥 Participantes
*   **Angelus Infernus** (@AngelusInfernus): Arquitectura de Sistemas y Estrategia de IA.
*   **Saoricoder** (@Saoricoder): Desarrollo Fullstack y Diseño de Experiencia de Usuario (UX/UI).

---

### 🌟 Sobre el Hack-i-athon 2026
El **[Hack-i-athon 2026](https://hackiathon.dev/): Inteligencia Artificial Generativa** es la tercera edición de la competencia de IA más grande del Ecuador. Organizado por **Viamatica**, **IT Ahora** y **Citytech**, con **Aseguradora del Sur** como Líder de Innovación, este evento busca:

*   **Fomentar el Talento Local:** Conectar a los mejores desarrolladores del país con los desafíos reales del sector corporativo.
*   **Enfoque en Agentes de IA:** El núcleo de esta edición es la creación de **Agentes Inteligentes** capaces de razonar y resolver problemas complejos.
*   **Impacto Social:** Crear soluciones que no solo sean técnicamente avanzadas, sino que tengan un impacto positivo y tangible en la sociedad.

Este proyecto, **Angelus Sentinel**, nace como una respuesta directa a la visión del evento, utilizando IA Generativa para humanizar y agilizar la atención médica de emergencia.

---

### 🏆 El Desafío: Tema 4 - Sistema de Alerta Temprana de Ingresos a Emergencias
**Descripción del Problema:** El ingreso a emergencias suele estar plagado de fricciones administrativas: validación manual de pólizas, verificación de preexistencias y falta de comunicación inmediata entre el hospital y la aseguradora. Estos retrasos pueden comprometer la atención del paciente.

**Nuestra Solución:**
Hemos construido un **Agente Autónomo** que actúa como un centinela digital. El sistema implementa un flujo de trabajo de "Cero Fricción":
1.  **Activación por Webhook:** El sistema se dispara automáticamente cuando un hospital registra un ingreso.
2.  **Triage Clínico-Administrativo:** Usando **Gemini Pro**, el agente analiza los síntomas (Triage) y cruza la información con la póliza del paciente en milisegundos.
3.  **Notificación Simultánea:** Envía alertas instantáneas y estructuradas tanto al departamento de admisiones del hospital como al gestor de casos de la aseguradora, permitiendo una autorización proactiva.
4.  **Centro de Monitoreo:** Una consola centralizada que visualiza cada evento y decisión del sistema para mantener la transparencia total.

---

## ⚙️ Sección 2: Tecnologías y Configuración del Entorno

### 🚀 Stack Tecnológico
*   **Backend:** FastAPI (Python 3.10+) - Alta velocidad y validación de tipos asíncrona.
*   **IA Cerebro:** Google Gemini Pro (Generative AI SDK).
*   **Base de Datos:** Firebase Firestore (NoSQL) para persistencia en tiempo real.
*   **Frontend:** Next.js 15 (App Router) + React 19 + TypeScript.
*   **Estilos:** Tailwind CSS con estética *Glassmorphism* y Dark Mode.
*   **Iconografía:** Lucide React.

### 🛠️ Configuración e Instalación

#### 1. Requisitos Previos
*   Python 3.10 o superior instalado.
*   Node.js 18 o superior instalado.
*   Cuenta de Google Cloud / Firebase (con API Key de Gemini).

#### 2. Configuración del Backend
1.  Navega a la carpeta `/backend`.
2.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # En Windows
    ```
3.  Instala las dependencias necesarias:
    ```bash
    pip install fastapi uvicorn google-generativeai firebase-admin python-dotenv pydantic
    ```
4.  Configura tu archivo `.env` en la raíz del proyecto:
    ```env
    GEMINI_API_KEY=tu_api_key_aqui
    FIREBASE_SERVICE_ACCOUNT_PATH=ruta/a/tu/firebase-key.json
    ```

#### 3. Configuración del Frontend
1.  Navega a la carpeta `/frontend`.
2.  Instala las dependencias:
    ```bash
    npm install
    ```
3.  Ejecuta el servidor de desarrollo:
    ```bash
    npm run dev
    ```

#### 4. Ejecución del Sistema
Para que el sistema funcione correctamente, ambos servidores deben estar activos:
*   **Backend:** `python -m backend.main` (Corre en `http://localhost:8000`)
*   **Frontend:** `npm run dev` (Corre en `http://localhost:3000`)

---

### 📡 Uso del Simulador (Tema 4)
Una vez en el dashboard, haz clic en el botón **"SIMULAR WEBHOOK (TEMA 4)"**. Esto disparará un evento de ingreso ficticio que demostrará cómo Angelus procesa, clasifica y notifica el siniestro de forma totalmente autónoma.

---
*Angelus Sentinel - Protegiendo lo que importa, cuando más importa.*
