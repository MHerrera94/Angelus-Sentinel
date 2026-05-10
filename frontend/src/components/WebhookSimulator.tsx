"use client";

import { useState } from "react";
import { Zap, Server, Loader2, UserCheck } from "lucide-react";

// Datos de prueba válidos basados en el seed del backend
const MOCK_PATIENTS = [
  {
    nombre: "Elena",
    apellido: "Narváez",
    ci: "0922222222",
    enfermedad: "Apendicitis Aguda",
    triaje: "Amarillo",
    posee_seguro: true,
    numero_seguro: "POL-GLOBAL-CARE"
  },
  {
    nombre: "Juan",
    apellido: "Pérez",
    ci: "0912345678",
    enfermedad: "Crisis asmática",
    triaje: "Rojo",
    posee_seguro: true,
    numero_seguro: "IESS General"
  },
  {
    nombre: "Roberto",
    apellido: "Gómez",
    ci: "1733333333",
    enfermedad: "Visión borrosa y dolor ocular",
    triaje: "Verde",
    posee_seguro: true,
    numero_seguro: "POL-PLATINUM"
  },
  {
    nombre: "Ana",
    apellido: "López",
    ci: "1234567890",
    enfermedad: "Descompensación diabética",
    triaje: "Amarillo",
    posee_seguro: true,
    numero_seguro: "POL-IESS-JUB"
  }
];

export default function WebhookSimulator() {
  const [isSimulating, setIsSimulating] = useState(false);
  const [lastPayload, setLastPayload] = useState<any>(null);

  const simulateRandomWebhook = () => {
    setIsSimulating(true);
    
    // Seleccionar paciente aleatorio
    const randomPatient = MOCK_PATIENTS[Math.floor(Math.random() * MOCK_PATIENTS.length)];
    setLastPayload(randomPatient);

    // Simular retraso de red
    setTimeout(() => {
      const formStr = `[WEBHOOK DE SEGUROS]
Nombre: ${randomPatient.nombre} ${randomPatient.apellido}
C.I: ${randomPatient.ci}
Triaje sugerido: ${randomPatient.triaje}
Diagnóstico inicial: ${randomPatient.enfermedad}
Póliza Automática: ${randomPatient.numero_seguro}`;

      // Emitir el mismo evento que el formulario, para que Angelus lo intercepte
      const event = new CustomEvent('sentinel-form-submit', { 
        detail: { 
          text: formStr, 
          formData: randomPatient 
        } 
      });
      window.dispatchEvent(event);
      
      setIsSimulating(false);
    }, 800);
  };

  return (
    <div className="glass-card flex flex-col h-full border-amber-100 bg-amber-50/30 overflow-hidden shadow-2xl p-6">
      <div className="flex items-center gap-3 mb-4 border-b border-amber-200/50 pb-4">
        <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center text-amber-600 shadow-inner">
          <Server size={20} />
        </div>
        <div className="flex-1">
          <h2 className="text-xl font-black text-slate-800 tracking-tight">Webhook de Emergencias</h2>
          <p className="text-[10px] text-amber-600 font-bold uppercase tracking-tighter">Integración B2B</p>
        </div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-start text-center p-4 overflow-y-auto w-full">
        <div className="w-24 h-24 bg-white rounded-full flex shrink-0 items-center justify-center shadow-lg border-4 border-amber-100 mb-6">
          <Zap size={40} className="text-amber-500" />
        </div>
        
        <h3 className="text-lg font-bold text-slate-700 mb-2">Simulador de Ingresos Automatizados</h3>
        <p className="text-sm text-slate-500 mb-8 max-w-[80%] mx-auto">
          En un entorno real, el sistema de triaje o pre-admisión del hospital envía automáticamente los datos del paciente a Angelus mediante Webhooks en cuanto cruzan la puerta de emergencias.
        </p>

        {lastPayload && (
          <div className="w-full bg-white p-4 rounded-xl border border-amber-100 mb-6 text-left shadow-sm animate-in fade-in slide-in-from-bottom-4 shrink-0">
            <div className="flex items-center gap-2 mb-2">
              <UserCheck size={16} className="text-emerald-500" />
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Último Payload Enviado</span>
            </div>
            <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
              <div><span className="text-slate-400 font-medium">Paciente:</span> <span className="font-bold text-slate-700">{lastPayload.nombre} {lastPayload.apellido}</span></div>
              <div><span className="text-slate-400 font-medium">C.I:</span> <span className="font-bold text-slate-700">{lastPayload.ci}</span></div>
              <div><span className="text-slate-400 font-medium">Póliza:</span> <span className="font-bold text-slate-700">{lastPayload.numero_seguro}</span></div>
              <div><span className="text-slate-400 font-medium">Motivo:</span> <span className="font-bold text-slate-700 truncate block">{lastPayload.enfermedad}</span></div>
            </div>
          </div>
        )}

        <button 
          onClick={simulateRandomWebhook}
          disabled={isSimulating}
          className="w-full shrink-0 bg-amber-500 hover:bg-amber-600 text-white font-black py-4 rounded-xl shadow-lg shadow-amber-500/30 transition-all active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-70 text-base uppercase tracking-widest mt-auto"
        >
          {isSimulating ? (
            <Loader2 className="animate-spin" size={20} />
          ) : (
            <>
              Simular Webhook
              <Server size={18} />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
