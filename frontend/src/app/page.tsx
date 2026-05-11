"use client";

import { ShieldAlert, CheckCircle, Zap, X } from "lucide-react";
import { useState, useEffect } from "react";
import SentinelChat from "@/components/SentinelChat";
import EmergencyForm from "@/components/EmergencyForm";
import HospitalNotifications from "@/components/HospitalNotifications";
import InsuranceNotifications from "@/components/InsuranceNotifications";

export default function Home() {
  const [logs, setLogs] = useState<any[]>([]);
  const [showTestUsers, setShowTestUsers] = useState(false);
  const [simulating, setSimulating] = useState(false);

  const fetchLogs = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/notifications", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000) // 5 second timeout
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setLogs(data || []);
    } catch (error) {
      console.error("Error fetching logs:", error);
      // Set empty array on error to prevent undefined issues
      setLogs([]);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  const simulateWebhook = async () => {
    setSimulating(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/webhook/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: "DEMO-" + Date.now(),
          hospital_id: "HOSP-01",
          emergency_type: "TRAUMA",
          symptoms: "Paciente crítico en emergencia"
        }),
        signal: AbortSignal.timeout(5000) // 5 second timeout
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Webhook response:", data);
      setTimeout(async () => {
        await fetchLogs();
      }, 500);
    } catch (error) {
      console.error("Simulación fallida:", error);
    } finally {
      setTimeout(() => setSimulating(false), 2000);
    }
  };

  return (
    <main className="h-screen max-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-50 via-blue-50 to-white flex flex-col overflow-hidden">
      {/* Compact Header */}
      <header className="bg-white/60 backdrop-blur-2xl border-b border-slate-200 h-12 flex-none px-6 py-2 z-50">
        <div className="flex items-center justify-between h-full">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center">
              <ShieldAlert size={20} className="text-cyan-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Angelus Sentinel</h1>
              <p className="text-sm font-medium text-slate-700 tracking-tight">Emergency Dashboard</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="relative">
              <button 
                onClick={() => setShowTestUsers(!showTestUsers)}
                disabled={simulating}
                className={`${
                  simulating 
                    ? 'bg-cyan-500 shadow-lg shadow-cyan-500/50' 
                    : 'bg-gradient-to-r from-cyan-500 to-emerald-500 hover:brightness-110'
                } text-white px-3 py-1 rounded-lg text-xs font-black transition-all active:scale-95 disabled:opacity-90`}
              >
                {simulating ? "Processing..." : "Usuarios de Prueba"}
              </button>
              
              {/* Test Users Popover */}
              {showTestUsers && (
                <div className="absolute top-full mt-2 right-0 z-50 w-80 bg-slate-900/60 backdrop-blur-xl border border-cyan-500/50 rounded-lg shadow-lg shadow-cyan-500/20">
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-cyan-300 text-sm font-black">Usuarios de Prueba</h3>
                      <button 
                        onClick={() => setShowTestUsers(false)}
                        className="text-cyan-400 hover:text-cyan-300 transition-colors"
                      >
                        <X size={16} />
                      </button>
                    </div>
                    <div className="space-y-2">
                      <div className="p-2 bg-slate-800/40 rounded-lg border border-white/10">
                        <p className="text-cyan-400 text-xs font-bold mb-1">Paciente 1:</p>
                        <p className="text-cyan-300 text-xs">Cédula: <span className="text-emerald-400 font-mono">1726354910</span></p>
                        <p className="text-cyan-300 text-xs">Nombre: <span className="text-emerald-400">Juan Pérez</span></p>
                        <p className="text-cyan-300 text-xs">Seguro: <span className="text-emerald-400 font-mono">SEG-987654</span></p>
                      </div>
                      <div className="p-2 bg-slate-800/40 rounded-lg border border-white/10">
                        <p className="text-cyan-400 text-xs font-bold mb-1">Paciente 2:</p>
                        <p className="text-cyan-300 text-xs">Cédula: <span className="text-emerald-400 font-mono">0912345678</span></p>
                        <p className="text-cyan-300 text-xs">Nombre: <span className="text-emerald-400">María García</span></p>
                        <p className="text-cyan-300 text-xs">Seguro: <span className="text-emerald-400 font-mono">SEG-123456</span></p>
                      </div>
                      <div className="p-2 bg-slate-800/40 rounded-lg border border-white/10">
                        <p className="text-cyan-400 text-xs font-bold mb-1">Paciente 3:</p>
                        <p className="text-cyan-300 text-xs">Cédula: <span className="text-emerald-400 font-mono">1711223344</span></p>
                        <p className="text-cyan-300 text-xs">Nombre: <span className="text-emerald-400">Carlos Rodríguez</span></p>
                        <p className="text-cyan-300 text-xs">Seguro: <span className="text-emerald-400 font-mono">SEG-555666</span></p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-2 px-2 py-1 bg-emerald-500/10 rounded-full border border-emerald-500/30">
              <div className="w-1 h-1 rounded-full bg-emerald-400 animate-pulse"></div>
              <span className="text-emerald-400 text-[10px] font-black">System active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Bento Grid Container */}
      <div className="grid grid-cols-2 grid-rows-[1.5fr_1fr] gap-4 flex-1 p-4 min-h-0">
        {/* Top Left: Patient Admission Entry */}
        <div className="flex flex-col h-full min-h-0">
          <EmergencyForm />
        </div>

        {/* Top Right: AI Chat Console */}
        <div className="flex flex-col h-full min-h-0">
          <SentinelChat />
        </div>

        {/* Bottom Left: Clinical Notifications */}
        <div className="flex flex-col h-full min-h-0">
          <HospitalNotifications logs={logs} />
        </div>

        {/* Bottom Right: Insurance Validation */}
        <div className="flex flex-col h-full min-h-0">
          <InsuranceNotifications logs={logs} />
        </div>
      </div>
    </main>
  );
}
