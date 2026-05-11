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

  const [currentAction, setCurrentAction] = useState<string>("");

  useEffect(() => {
    const statusInterval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/status");
        const data = await res.json();
        if (data.is_active && data.action) {
          setCurrentAction(data.action);
        } else {
          setCurrentAction("");
        }
      } catch (e) {
        // silenciar errores
      }
    }, 600);
    return () => clearInterval(statusInterval);
  }, []);

  useEffect(() => {
    const handleFormSubmit = (e: Event) => {
      const customEvent = e as CustomEvent;
      const { text, formData } = customEvent.detail;
      // Usamos el texto pre-formateado del formulario o construimos uno
      sendMessage(text, undefined, formData);
    };
    window.addEventListener('sentinel-form-submit', handleFormSubmit);
    return () => window.removeEventListener('sentinel-form-submit', handleFormSubmit);
  }, [operatorName]);

  return (
    <div className="glass-card flex flex-col h-full border-indigo-200 bg-white overflow-hidden shadow-2xl rounded-3xl">
      {/* Chat Header */}
      <div className="bg-indigo-600 p-4 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-2xl flex items-center justify-center text-white backdrop-blur-sm shadow-inner">
            <Cpu size={24} className="animate-pulse" />
          </div>
          <div className="flex flex-col">
            <h2 className="text-white text-lg font-black uppercase tracking-widest leading-none mb-1">Núcleo Angelus</h2>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-ping"></div>
              <span className="text-indigo-100 text-[9px] font-bold uppercase tracking-tighter opacity-80">Coordinación Activa</span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-[9px] font-black text-indigo-200 uppercase opacity-60">Operador</span>
          <input 
            type="text" 
            value={operatorName}
            onChange={(e) => setOperatorName(e.target.value)}
            className="text-white font-bold text-xs bg-indigo-500/40 px-2 py-1 rounded-lg border border-indigo-400/30 outline-none focus:ring-2 focus:ring-white/50 w-24 text-right"
          />
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-slate-50/30 custom-scrollbar">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-500`}>
            <div className={`max-w-[88%] flex gap-3 ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
              <div className={`w-8 h-8 rounded-xl flex-shrink-0 flex items-center justify-center shadow-lg ${
                m.role === "user" ? "bg-slate-700 text-white" : "bg-indigo-600 text-white"
              }`}>
                {m.role === "user" ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className={`flex flex-col gap-2 ${m.role === "user" ? "items-end" : "items-start"}`}>
                <div 
                  className={`p-4 rounded-2xl shadow-sm border ${
                    m.role === "user" 
                      ? "bg-white border-slate-200 text-slate-800 rounded-tr-none" 
                      : "bg-indigo-600 border-indigo-500 text-white rounded-tl-none"
                  }`}
                  style={m.color ? { borderLeft: `6px solid ${m.color}`, paddingLeft: '15px' } : {}}
                >
                  {m.type === "RESULT" ? (
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 border-b border-white/20 pb-2">
                        <Shield size={16} className="text-white" />
                        <span className="font-black uppercase tracking-widest text-xs">Validación Angelus</span>
                      </div>
                      <p className="text-sm leading-relaxed font-medium italic">"{m.content}"</p>
                      <div className="grid grid-cols-2 gap-3 text-[10px]">
                        <div className="bg-white/10 p-2 rounded-xl border border-white/10">
                          <span className="block text-indigo-200 uppercase font-bold text-[9px]">Póliza</span>
                          <span className="text-white font-black">ACTIVA</span>
                        </div>
                        <div className="bg-white/10 p-2 rounded-xl border border-white/10">
                          <span className="block text-indigo-200 uppercase font-bold text-[9px]">Triage</span>
                          <span className="font-black" style={{ color: m.color }}>OK</span>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm leading-relaxed font-medium">{m.content}</p>
                  )}
                </div>
                
                {(m.type === "DISAMBIGUATION" || m.type === "QUESTION") && m.options && (
                  <div className="flex flex-col gap-2 mt-2 w-full">
                    {m.options.map((opt, oi) => (
                      <button
                        key={oi}
                        onClick={() => sendMessage(`Confirmado: ${opt.label}`, opt.id)}
                        className="bg-white hover:bg-indigo-50 border border-indigo-100 text-indigo-600 font-black py-2 px-4 rounded-xl text-xs transition-all hover:scale-[1.01] active:scale-95 text-left shadow-sm flex items-center justify-between group"
                      >
                        {opt.label}
                        <CheckCircle2 size={14} className="opacity-0 group-hover:opacity-100 transition-all -translate-x-1 group-hover:translate-x-0" />
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {(loading || currentAction) && (
          <div className="flex justify-start">
             <div className="bg-indigo-100/50 p-3 rounded-2xl rounded-tl-none border border-indigo-200/30 flex items-center gap-2">
                <Loader2 className="animate-spin text-indigo-600" size={16} />
                <span className="text-xs text-indigo-600 font-black italic uppercase tracking-tighter">
                  {currentAction || "Sincronizando..."}
                </span>
              </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-5 bg-white border-t border-slate-100 shadow-xl">
        <div className="relative flex items-center gap-3 bg-slate-100 p-1.5 rounded-[2rem] border-2 border-transparent focus-within:border-indigo-500 transition-all shadow-inner">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
            placeholder="Escriba aquí..."
            className="flex-1 bg-transparent border-none focus:ring-0 px-5 py-2 text-sm text-slate-700 font-medium placeholder:text-slate-400"
            disabled={loading}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={loading || !input.trim()}
            className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-full shadow-lg shadow-indigo-500/40 transition-all active:scale-90 disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </div>
        <p className="text-[9px] text-center mt-3 text-slate-400 font-black uppercase tracking-widest opacity-60">
          Sentinel Protocol V2 • Medical Grade IA
        </p>
      </div>
    </div>
  );
}
