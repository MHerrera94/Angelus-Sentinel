import React from 'react';
import { ShieldCheck, FileText, Clock, Zap } from 'lucide-react';

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

export default function InsuranceNotifications({ logs }: Props) {
  const insuranceLogs = logs.filter(log => log.type === 'INSURANCE');

  return (
    <div className="flex flex-col h-full border-[3px] border-indigo-600 bg-white rounded-3xl overflow-hidden shadow-2xl transition-all">
      <div className="bg-indigo-600 p-6 flex items-center gap-4">
        <div className="bg-white/20 p-3 rounded-2xl">
          <ShieldCheck className="text-white" size={28} />
        </div>
        <div>
          <h2 className="text-white text-xl font-black uppercase tracking-widest">Canal Administrativo (Seguro)</h2>
          <p className="text-indigo-100 text-[10px] font-bold uppercase opacity-80">Validación de Coberturas en Tiempo Real</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar bg-indigo-50/30">
        {insuranceLogs.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-300 gap-4 opacity-60">
            <Zap size={64} className="animate-pulse" />
            <p className="font-bold italic text-lg uppercase tracking-tighter">Esperando eventos de siniestro...</p>
          </div>
        ) : (
          insuranceLogs.map((log, index) => (
            <div key={index} className="bg-white border-2 border-indigo-100 p-5 rounded-2xl shadow-sm hover:shadow-md transition-all animate-in slide-in-from-left-4">
              <div className="flex justify-between items-start mb-3">
                <span className="text-[10px] font-black text-indigo-500 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-500 bg-emerald-50 px-2 py-1 rounded-md">
                  <Clock size={12} /> SINIESTRO REGISTRADO
                </span>
              </div>
              <p className="text-slate-800 font-bold text-base leading-tight mb-3">
                {log.message}
              </p>
              {log.payload && (
                <div className="bg-indigo-50/50 rounded-xl p-4 border border-indigo-100">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Cobertura</p>
                      <p className="text-sm font-black text-indigo-700 uppercase">{log.payload.decision}</p>
                    </div>
                    <div>
                      <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Póliza</p>
                      <p className="text-sm font-black text-slate-700">{log.payload.insurance_status?.id || 'NO IDENTIFICADA'}</p>
                      {log.payload.insurance_status?.detalles && (
                        <div className="mt-1 space-y-0.5">
                          {log.payload.insurance_status.detalles.map((d: string, i: number) => (
                            <p key={i} className="text-[9px] font-medium text-indigo-400 truncate">{d}</p>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="mt-3 border-t border-indigo-100 pt-3">
                    <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter mb-1">Síntomas / Causa del Siniestro</p>
                    <p className="text-xs font-bold text-indigo-900 italic">
                      {log.payload.symptoms || 'Análisis de emergencia en curso'}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
