import React, { useState, useEffect } from 'react';
import { Stethoscope, Activity, Clock } from 'lucide-react';

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
  const [admittedPatients, setAdmittedPatients] = useState<any[]>([]);

  useEffect(() => {
    const handlePatientAdmitted = (e: Event) => {
      const customEvent = e as CustomEvent;
      const patientData = customEvent.detail;
      
      setAdmittedPatients(prev => [...prev, {
        id: patientData.patientId,
        name: patientData.patientName,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        type: 'Admitted',
        hospitalName: patientData.hospitalName || 'HOSP-METROPOLITANO'
      }]);
    };

    window.addEventListener('patient-admitted', handlePatientAdmitted);
    return () => window.removeEventListener('patient-admitted', handlePatientAdmitted);
  }, []);

  return (
    <div className="bg-white/30 backdrop-blur-2xl border border-white/10 rounded-[2rem] flex flex-col h-full min-h-0 overflow-hidden border-t-2 border-t-emerald-400/30 p-6 shadow-xl shadow-slate-200/50">
      <div className="bg-white/60 backdrop-blur-sm p-3 flex items-center gap-3 border-b border-white/10">
        <div className="bg-cyan-500/20 p-2 rounded-lg">
          <Stethoscope className="text-cyan-400" size={16} />
        </div>
        <div>
          <h2 className="text-slate-800 text-xs font-bold tracking-tight leading-tight">Departamento de Admisiones del Hospital</h2>
          <p className="text-slate-600 text-[8px] font-medium opacity-80 leading-tight">Real-time Admissions Processing</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-hidden bg-white/20 flex flex-col min-h-0 scale-90">
        {hospitalLogs.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-700 gap-2 overflow-y-auto scrollbar-thin scrollbar-track-slate-200/20 scrollbar-thumb-emerald-500/30 hover:scrollbar-thumb-emerald-500/50">
            <Activity size={32} className="animate-pulse" />
            {/* Static Alerts */}
            <div className="mt-2 space-y-1 w-full">
              {admittedPatients.length > 0 && (
                <div className="space-y-1">
                  {admittedPatients.map((patient, index) => (
                    <div key={index} className="flex items-center justify-between bg-emerald-500/10 rounded-lg px-2 py-1 border border-emerald-500/20">
                      <span className="text-emerald-400 text-xs font-medium leading-tight">{patient.time}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-emerald-300 text-xs font-bold leading-tight">{patient.name}</span>
                        <span className="text-emerald-500 text-[10px] leading-tight">ID: {patient.id}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              <div className="flex items-center justify-between bg-white/20 rounded-lg px-2 py-1 border border-slate-300">
                <span className="text-slate-600 text-xs font-medium leading-tight tracking-tight">10:45 AM</span>
                <span className="text-slate-700 text-xs font-bold leading-tight tracking-tight">Vitals Alert</span>
              </div>
              <div className="flex items-center justify-between bg-white/20 rounded-lg px-2 py-1 border border-slate-300">
                <span className="text-slate-600 text-xs font-medium leading-tight tracking-tight">09:30 AM</span>
                <span className="text-slate-700 text-xs font-bold leading-tight tracking-tight">ECG Monitor</span>
              </div>
              <div className="flex items-center justify-between bg-white/20 rounded-lg px-2 py-1 border border-slate-300">
                <span className="text-slate-600 text-xs font-medium leading-tight tracking-tight">08:15 AM</span>
                <span className="text-slate-700 text-xs font-bold leading-tight tracking-tight">Pressure Check</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-3 space-y-1 scrollbar-thin scrollbar-track-slate-200/20 scrollbar-thumb-emerald-500/30 hover:scrollbar-thumb-emerald-500/50">
            {hospitalLogs.slice(-5).map((log, index) => (
              <div key={index} className="bg-white/20 border border-slate-300 p-2 rounded-lg shadow-sm hover:shadow-md transition-all animate-in slide-in-from-right-4 backdrop-blur-sm">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-[8px] font-black text-slate-600 bg-white/40 px-2 py-1 rounded-full border border-slate-300 backdrop-blur-sm leading-tight tracking-tight">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="flex items-center gap-1 text-[8px] font-bold text-slate-600 leading-tight tracking-tight">
                    <Clock size={8} /> ACTIVE
                  </span>
                </div>
                <p className="text-slate-800 text-xs font-bold leading-tight mb-1">
                  {log.message}
                </p>
                {log.payload && (
                  <div className="bg-white/10 rounded-lg p-2 border border-slate-300 backdrop-blur-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <p className="text-[8px] font-bold text-slate-600 uppercase tracking-tighter leading-tight">Priority</p>
                        <p className="text-xs font-black text-slate-700 leading-tight">{log.payload.triage_priority}</p>
                      </div>
                      <div>
                        <p className="text-[8px] font-bold text-slate-600 uppercase tracking-tighter leading-tight">Identity</p>
                        <p className="text-xs font-black text-emerald-400 uppercase leading-tight">Validated</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
        {/* Botón "Verificar todas las alertas" */}
        {admittedPatients.length > 0 && (
          <div className="p-2 border-t border-white/10">
            <button className="w-full bg-cyan-500/10 border border-cyan-500/50 text-cyan-400 text-[10px] font-black py-1 px-2 rounded-lg hover:bg-cyan-500/20 transition-all leading-tight">
              Verificar todas las alertas
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
