"use client";

import { useState, useEffect, useRef } from "react";
import { Send, Activity, User, Bot, Loader2, CheckCircle2, AlertCircle, Shield, Cpu } from "lucide-react";

interface Message {
  role: "user" | "angelus";
  content: string;
  type?: "QUESTION" | "DISAMBIGUATION" | "RESULT" | "ERROR";
  color?: string;
  options?: { id: string; label: string }[];
}

export default function SentinelChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "angelus",
      content: "Núcleo Angelus activo. Reporte el ingreso del paciente para iniciar el protocolo de validación.",
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [operatorName, setOperatorName] = useState("Saoricoder");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // const scrollToBottom = () => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // };

  // useEffect(() => {
  //   scrollToBottom();
  // }, [messages]);

  const sendMessage = async (text: string, confirmedId?: string, formData?: any) => {
    if (!text && !confirmedId) return;

    if (text) {
      setMessages(prev => [...prev, { role: "user", content: text }]);
      setInput("");
    }

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          operator_name: operatorName,
          confirmed_patient_id: confirmedId,
          form_data: formData
        })
      });
      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: "angelus", 
        content: data.reply,
        type: data.type,
        color: data.color,
        options: data.options
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: "angelus", 
        content: "Error de conexión con el núcleo central.",
        type: "ERROR"
      }]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleFormSubmit = (e: Event) => {
      const customEvent = e as CustomEvent;
      const formData = customEvent.detail.formData;
      
      // Clear chat and start new admission flow
      setMessages([]);
      
      // Sequential AI Agent logic - Reto 4 Flow
      const processPatientAdmission = async () => {
        // 1. First message: "Validando póliza..."
        await sendMessage("Validando póliza...");
        
        // 2. Wait 1.5s then send validation result
        setTimeout(async () => {
          const validationResult = "Éxito: Póliza validada automáticamente";
          await sendMessage(validationResult);
          
          // 3. Wait another 1.5s then check preexistencias
          setTimeout(async () => {
            await sendMessage(`Revisando historial de preexistencias para paciente [${formData.nombre}]...`);
            
            // 4. Fetch and display previous medical history
            setTimeout(async () => {
              try {
                const response = await fetch(`http://localhost:8000/patients/${formData.ci}`);
                if (response.ok) {
                  const patientData = await response.json();
                  if (patientData && patientData.medical_history && patientData.medical_history.length > 0) {
                    await sendMessage(`Se encontraron ${patientData.medical_history.length} atenciones previas:`);
                    patientData.medical_history.forEach((record: any, index: number) => {
                      setTimeout(async () => {
                        await sendMessage(`• ${record.date} - ${record.type}: ${record.description}`);
                      }, index * 800);
                    });
                  } else {
                    await sendMessage("No se encontraron atenciones previas en el historial.");
                  }
                }
              } catch (error) {
                await sendMessage("Error al consultar historial médico.");
              }
              
              // 5. Update other components if validation successful
              setTimeout(() => {
                if (formData.numero_seguro) {
                  // Trigger updates to Clinical Channel and Insurance Validation
                  const updateEvent = new CustomEvent('patient-admitted', {
                    detail: {
                      patientId: formData.ci,
                      patientName: formData.nombre,
                      hasInsurance: true,
                      policyNumber: formData.numero_seguro,
                      hospitalName: "HOSP-METROPOLITANO"
                    }
                  });
                  window.dispatchEvent(updateEvent);
                }
              }, 1500);
            }, 1500);
          }, 1500);
        }, 1500);
      };
      
      processPatientAdmission();
    };
    
    window.addEventListener('sentinel-form-submit', handleFormSubmit);
    return () => window.removeEventListener('sentinel-form-submit', handleFormSubmit);
  }, [operatorName]);

  return (
    <div className="bg-white/30 backdrop-blur-2xl border border-white/10 rounded-[2rem] flex flex-col h-full min-h-0 overflow-hidden border-t-2 border-t-cyan-400/30 p-6 shadow-xl shadow-slate-200/50">
      {/* Chat Header */}
      <div className="bg-white/60 backdrop-blur-sm p-3 flex items-center justify-between border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center">
            <Cpu size={20} className="animate-pulse text-cyan-400" />
          </div>
          <div className="flex flex-col">
            <h2 className="text-slate-800 text-sm font-bold tracking-tight">Núcleo Neural de IA</h2>
            <div className="flex items-center gap-2">
              <div className="w-1 h-1 rounded-full bg-cyan-400 animate-ping"></div>
              <span className="text-slate-600 text-[8px] font-bold uppercase tracking-tighter">Procesando...</span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-slate-600 text-[8px] font-bold text-slate-500 uppercase opacity-60">Operator</span>
          <input 
            type="text" 
            value={operatorName}
            onChange={(e) => setOperatorName(e.target.value)}
            className="text-slate-700 font-bold text-xs bg-white/60 px-2 py-1 rounded-lg border border-slate-300 outline-none focus:ring-2 focus:ring-cyan-400/30 w-20 text-right backdrop-blur-sm"
          />
        </div>
      </div>

      {/* Messages Area - Fixed Height */}
      <div className="flex-1 overflow-hidden flex flex-col bg-white/20">
        {/* Neural Wave Animation */}
        <div className="flex items-center justify-center p-4">
          <div className="relative w-32 h-16">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="flex gap-1">
                {[...Array(20)].map((_, i) => (
                  <div
                    key={i}
                    className="w-1 bg-cyan-400 rounded-full animate-pulse"
                    style={{
                      height: `${Math.sin((i * Math.PI) / 10) * 20 + 20}px`,
                      animationDelay: `${i * 0.1}s`,
                      opacity: 0.3 + (Math.sin((i * Math.PI) / 10) + 1) * 0.35
                    }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
        <span className="text-slate-600 text-xs font-black ml-2">Procesando...</span>
        
        {/* Messages Container with Internal Scroll */}
        <div className="flex-grow overflow-y-auto p-2 space-y-2 scrollbar-thin scrollbar-track-slate-200/20 scrollbar-thumb-cyan-500/30 hover:scrollbar-thumb-cyan-500/50">
          {messages.slice(-3).map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-500`}>
              <div className={`max-w-[85%] flex gap-2 ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                <div className={`w-6 h-6 rounded-lg flex-shrink-0 flex items-center justify-center ${
                  m.role === "user" ? "bg-slate-700 text-white" : "bg-cyan-600 text-white"
                }`}>
                  {m.role === "user" ? <User size={12} /> : <Bot size={12} />}
                </div>
                <div className={`flex flex-col gap-1 ${m.role === "user" ? "items-end" : "items-start"}`}>
                  <div 
                    className={`p-2 rounded-lg border backdrop-blur-sm ${
                      m.role === "user" 
                        ? "bg-slate-100/40 border-slate-300 text-slate-800 rounded-tr-none" 
                        : "bg-cyan-500/10 border-cyan-500/20 text-cyan-800 rounded-tl-none"
                    }`}
                  >
                    <div className="flex items-start gap-2">
                    <span className={`text-xs font-bold ${m.role === 'user' ? 'text-slate-600' : 'text-cyan-700'}`}>
                      {m.role === 'user' ? 'Operador:' : 'Ángelus IA:'}
                    </span>
                    <p className="text-xs leading-relaxed font-medium text-slate-700 flex-1">{m.content}</p>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
               <div className="bg-cyan-500/10 p-2 rounded-lg rounded-tl-none border border-cyan-500/20 flex items-center gap-2 backdrop-blur-sm">
                  <Loader2 className="animate-spin text-cyan-400" size={12} />
                  <div className="flex items-start gap-2">
                    <span className="text-xs font-bold text-cyan-700">Ángelus IA:</span>
                    <span className="text-xs text-cyan-600 font-black italic">Sincronizando...</span>
                  </div>
                </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="p-2 bg-white/60 backdrop-blur-sm border-t border-white/10">
        <div className="relative flex items-center gap-2 bg-white/80 p-1 rounded-lg border border-slate-300 focus-within:border-cyan-400 transition-all backdrop-blur-sm">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
            placeholder="Type here..."
            className="flex-1 bg-transparent border-none focus:ring-0 px-3 py-1 text-sm text-slate-700 font-medium placeholder:text-slate-500/60"
            disabled={loading}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-cyan-500 to-emerald-500 hover:brightness-110 transition-all text-white p-1 rounded-lg active:scale-95 disabled:opacity-50"
          >
            <Send size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
