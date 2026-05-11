import React, { useState, useEffect } from 'react';
import { ShieldCheck, FileText, Clock, Zap, CheckCircle } from 'lucide-react';

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
  const [validatedPolicies, setValidatedPolicies] = useState<any[]>([]);

  useEffect(() => {
    const handlePatientAdmitted = (e: Event) => {
      const customEvent = e as CustomEvent;
      const patientData = customEvent.detail;
      
      if (patientData.hasInsurance) {
        setValidatedPolicies(prev => [...prev, {
          patientId: patientData.patientId,
          patientName: patientData.patientName,
          policyNumber: patientData.policyNumber,
          insuranceCompany: 'Sentinel Health',
          validationCode: `VAL-${Date.now().toString().slice(-6)}`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          status: 'Validated'
        }]);
      }
    };

    window.addEventListener('patient-admitted', handlePatientAdmitted);
    return () => window.removeEventListener('patient-admitted', handlePatientAdmitted);
  }, []);

  return (
    <div className="bg-white/30 backdrop-blur-2xl border border-white/10 rounded-[2rem] flex flex-col h-full min-h-0 overflow-hidden border-t-2 border-t-emerald-400/30 p-6 shadow-xl shadow-slate-200/50">
      <div className="bg-white/60 backdrop-blur-sm p-3 flex items-center gap-3 border-b border-white/10">
        <div className="bg-cyan-500/20 p-2 rounded-lg">
          <ShieldCheck className="text-cyan-400" size={16} />
        </div>
        <div>
          <h2 className="text-slate-800 text-xs font-bold tracking-tight leading-tight">Validación de Seguro</h2>
          <p className="text-slate-600 text-[8px] font-medium opacity-80 leading-tight">Real-time Coverage Validation</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-hidden bg-white/20 flex flex-col min-h-0 scale-90">
        {insuranceLogs.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-700 gap-2 overflow-y-auto scrollbar-thin scrollbar-track-slate-200/20 scrollbar-thumb-emerald-500/30 hover:scrollbar-thumb-emerald-500/50">
            {/* Validated Policies */}
            {validatedPolicies.length > 0 && (
              <div className="w-full space-y-1">
                {validatedPolicies.map((policy, index) => (
                  <div key={index} className="bg-emerald-500/10 rounded-lg px-2 py-1 border border-emerald-500/20">
                    <div className="flex items-center justify-between">
                      <span className="text-emerald-400 text-xs font-medium leading-tight">{policy.time}</span>
                      <span className="text-emerald-300 text-xs font-bold leading-tight">{policy.status}</span>
                    </div>
                    <p className="text-emerald-400 text-xs mt-1 leading-tight">{policy.patientName}</p>
                    <p className="text-emerald-500 text-[10px] leading-tight">Policy: {policy.policyNumber}</p>
                    <div className="text-cyan-400 text-[10px] mt-1 space-y-0.5 leading-tight">
                      <p>{policy.insuranceCompany}</p>
                      <p>Validation Code: {policy.validationCode}</p>
                      <p>Validación confirmada para el paciente {policy.patientId}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Large Centered Check for Impact */}
            <div className="w-8 h-8 bg-emerald-500/20 rounded-full flex items-center justify-center border border-emerald-500/30">
              <CheckCircle className="text-emerald-400" size={16} />
            </div>
            <div className="text-center">
              <p className="text-lg font-black text-emerald-400 leading-tight">Active</p>
              <p className="text-xs text-slate-600 leading-tight">Coverage Status</p>
            </div>
            <div className="text-center mt-1">
              <p className="text-xs text-slate-600 font-bold leading-tight">Sentinel Health</p>
              <p className="text-xs text-slate-600 leading-tight">Premium Plan</p>
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-3 space-y-1 scrollbar-thin scrollbar-track-slate-200/20 scrollbar-thumb-emerald-500/30 hover:scrollbar-thumb-emerald-500/50">
            {insuranceLogs.slice(-3).map((log, index) => (
              <div key={index} className="bg-white/20 border border-slate-300 p-2 rounded-lg shadow-sm hover:shadow-md transition-all animate-in slide-in-from-left-4 backdrop-blur-sm">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-[8px] font-black text-slate-600 bg-white/40 px-2 py-1 rounded-full border border-slate-300 backdrop-blur-sm leading-tight tracking-tight">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="flex items-center gap-1 text-[8px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-md backdrop-blur-sm leading-tight">
                    <Clock size={8} /> CLAIM
                  </span>
                </div>
                <p className="text-slate-800 text-xs font-bold leading-tight mb-1">
                  {log.message}
                </p>
                {log.payload && (
                  <div className="bg-white/10 rounded-lg p-2 border border-slate-300 backdrop-blur-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <p className="text-[8px] font-bold text-slate-600 uppercase tracking-tighter leading-tight">Coverage</p>
                        <p className="text-xs font-black text-emerald-300 leading-tight">{log.payload.decision}</p>
                      </div>
                      <div>
                        <p className="text-[8px] font-bold text-slate-600 uppercase tracking-tighter leading-tight">Policy</p>
                        <p className="text-xs font-black text-slate-700 leading-tight">{log.payload.insurance_status?.id || 'N/A'}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
