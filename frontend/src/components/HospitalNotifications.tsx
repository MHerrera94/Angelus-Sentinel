import React from 'react';
import { Hospital, Activity, Stethoscope, Clock } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  target?: string;
  message: string;
  type?: string;
  status: string;
  payload?: any;
}

interface Props {
  logs: LogEntry[];
}

export default function HospitalNotifications({ logs }: Props) {
  const hospitalLogs = logs.filter(log => log.type === 'HOSPITAL');

  return (
    <div className="flex flex-col h-full border-[3px] border-rose-600 bg-white rounded-3xl overflow-hidden shadow-2xl transition-all">
      <div className="bg-rose-600 p-6 flex items-center gap-4">
        <div className="bg-white/20 p-3 rounded-2xl">
          <Stethoscope className="text-white" size={28} />
        </div>
        <div>
          <h2 className="text-white text-xl font-black uppercase tracking-widest">Canal Clínico (Hospital)</h2>
          <p className="text-rose-100 text-[10px] font-bold uppercase opacity-80">Alertas Médicas en Tiempo Real</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar bg-rose-50/30">
        {hospitalLogs.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-rose-300 gap-4 opacity-60">
            <Activity size={64} className="animate-pulse" />
            <p className="font-bold italic text-lg uppercase tracking-tighter">Esperando telemetría de admisión...</p>
          </div>
        ) : (
          hospitalLogs.map((log, index) => (
            <div key={index} className="bg-white border-2 border-rose-100 p-5 rounded-2xl shadow-sm hover:shadow-md transition-all animate-in slide-in-from-right-4">
              <div className="flex justify-between items-start mb-3">
                <span className="text-[10px] font-black text-rose-500 bg-rose-50 px-3 py-1 rounded-full border border-rose-100">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className="flex items-center gap-1 text-[10px] font-bold text-slate-400">
                  <Clock size={12} /> SISTEMA ACTIVO
                </span>
              </div>
              <p className="text-slate-800 font-bold text-base leading-tight mb-3">
                {log.message}
              </p>
              {log.payload && (
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Prioridad Triage</p>
                      <p className="text-sm font-black" style={{ color: log.payload.triage_color || '#e11d48' }}>
                        {log.payload.triage_priority}
                      </p>
                    </div>
                    <div>
                      <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Identidad</p>
                      <p className="text-sm font-black text-emerald-600 uppercase">Validada</p>
                    </div>
                  </div>
                  
                  <div className="border-t border-slate-200 pt-3">
                    <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter mb-1">Motivo de Ingreso / Síntomas</p>
                    <p className="text-xs font-bold text-slate-700 italic">
                      "{log.payload.motivo_ingreso || 'No especificado'}"
                    </p>
                  </div>

                  {log.payload.historial_interno && log.payload.historial_interno.length > 0 && (
                    <div className="border-t border-slate-200 pt-3">
                      <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter mb-1">Alertas de Historial (Sentinel)</p>
                      <div className="flex flex-wrap gap-1">
                        {log.payload.historial_interno.map((h: string, i: number) => (
                          <span key={i} className="text-[9px] font-bold bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md border border-rose-200">
                            {h}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
