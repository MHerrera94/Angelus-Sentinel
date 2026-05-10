"use client";

import { ShieldAlert, CheckCircle, Zap } from "lucide-react";
import { useState, useEffect } from "react";
import SentinelChat from "@/components/SentinelChat";
import EmergencyForm from "@/components/EmergencyForm";
import HospitalNotifications from "@/components/HospitalNotifications";
import InsuranceNotifications from "@/components/InsuranceNotifications";
import WebhookSimulator from "@/components/WebhookSimulator";

export default function Home() {
  const [logs, setLogs] = useState<any[]>([]);
  const [simulating, setSimulating] = useState(false);
  const [activeTab, setActiveTab] = useState<"form" | "webhook">("webhook");

  const fetchLogs = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/notifications");
      const data = await response.json();
      setLogs(data);
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(() => {
      fetchLogs();
    }, 3000); // Polling faster to show notifications
    return () => clearInterval(interval);
  }, []);

  const simulateWebhook = async () => {
    setSimulating(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/webhook/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: "0912345678",
          hospital_id: "HOSP-METROPOLITANO",
          emergency_type: "Pérdida de conciencia repentina",
          operator_name: "SISTEMA_WEBHOOK"
        })
      });
      
      if (response.ok) {
        setTimeout(async () => {
          await fetchLogs();
        }, 500);
      }
    } catch (error) {
      console.error("Simulación fallida:", error);
    } finally {
      setTimeout(() => setSimulating(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Navigation Header */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
                <ShieldAlert size={24} />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold font-heading leading-none text-slate-800 tracking-tighter">Emergencia Hospital Sentinel</span>
                <span className="text-[10px] font-bold text-primary tracking-widest uppercase opacity-80">Console Layer 3</span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="badge-online">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                Sistema Monitoreo Activo
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Grid Content */}
      <main className="max-w-[1700px] w-full mx-auto p-4 flex-1 flex flex-col gap-4 overflow-hidden">
        
        {/* Fila 1: Chat vs Inputs */}
        <div className="grid grid-cols-2 gap-6 h-[50vh]">
          {/* Cuadrante Superior Izquierdo: Chat */}
          <div className="flex flex-col h-full min-h-0">
            <SentinelChat />
          </div>

          {/* Cuadrante Superior Derecho: Contenedor con Tabs */}
          <div className="flex flex-col h-full min-h-0 relative bg-white rounded-3xl shadow-2xl overflow-hidden border border-slate-200">
            
            {/* Tabs Header */}
            <div className="flex w-full border-b border-slate-100 bg-slate-50/50 p-2 gap-2">
              <button 
                onClick={() => setActiveTab("form")}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-black uppercase tracking-wider transition-all flex items-center justify-center gap-2 ${activeTab === 'form' ? 'bg-white text-rose-600 shadow-sm border border-slate-200' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100/50'}`}
              >
                Formulario Manual
              </button>
              <button 
                onClick={() => setActiveTab("webhook")}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-black uppercase tracking-wider transition-all flex items-center justify-center gap-2 ${activeTab === 'webhook' ? 'bg-white text-amber-600 shadow-sm border border-slate-200' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100/50'}`}
              >
                Simular Webhook (B2B)
              </button>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-hidden relative">
              {activeTab === "form" ? (
                <div className="absolute inset-0 overflow-y-auto w-full h-full p-2">
                  <EmergencyForm />
                </div>
              ) : (
                <div className="absolute inset-0 overflow-y-auto w-full h-full p-2">
                  <WebhookSimulator />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Fila 2: Notificaciones Hospital vs Seguro */}
        <div className="grid grid-cols-2 gap-6 h-[32vh]">
          {/* Cuadrante Inferior Izquierdo: Hospital Notifications */}
          <div className="flex flex-col h-full min-h-0">
            <HospitalNotifications logs={logs} />
          </div>

          {/* Cuadrante Inferior Derecho: Insurance Notifications */}
          <div className="flex flex-col h-full min-h-0">
            <InsuranceNotifications logs={logs} />
          </div>
        </div>
      </main>
    </div>
  );
}
