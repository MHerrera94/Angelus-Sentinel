"use client";

import { useState } from "react";
import { Send, AlertTriangle, ShieldCheck, Loader2 } from "lucide-react";

export default function EmergencyForm() {
  const [formData, setFormData] = useState({
    nombre: "",
    apellido: "",
    ci: "",
    enfermedad: "",
    triaje: "Verde",
    posee_seguro: false,
    numero_seguro: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const formStr = `[FORMULARIO DE INGRESO]
Nombre: ${formData.nombre} ${formData.apellido}
C.I: ${formData.ci || 'No proporcionado'}
Triaje: ${formData.triaje}
Síntomas: ${formData.enfermedad}
Seguro: ${formData.posee_seguro ? "Sí (Póliza: " + formData.numero_seguro + ")" : "No"}`;

      const event = new CustomEvent('sentinel-form-submit', { 
        detail: { 
          text: formStr, 
          formData: formData 
        } 
      });
      window.dispatchEvent(event);
      
      // Notificar éxito visualmente o mantener datos
      // setFormData(prev => ({...prev, enfermedad: "", ci: "", numero_seguro: ""}));
      
    } catch (error) {
      console.error("Error al procesar formulario:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  return (
    <div className="glass-card flex flex-col h-full border-indigo-100 bg-white overflow-hidden shadow-2xl p-6">
      <div className="flex items-center gap-3 mb-4 border-b pb-4">
        <div className="w-10 h-10 bg-rose-100 rounded-xl flex items-center justify-center text-rose-600 shadow-inner">
          <AlertTriangle size={20} />
        </div>
        <div className="flex-1">
          <h2 className="text-xl font-black text-slate-800 tracking-tight">Registro de Admisión</h2>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">Pacientes Críticos</p>
        </div>
        <button 
          type="button"
          onClick={() => setFormData({
            nombre: "",
            apellido: "",
            ci: "",
            enfermedad: "",
            triaje: "Verde",
            posee_seguro: false,
            numero_seguro: "",
          })}
          className="text-[10px] font-black text-slate-400 hover:text-rose-500 uppercase tracking-widest transition-colors flex items-center gap-1 border border-slate-200 px-2 py-1 rounded-md"
        >
          Limpiar
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto pr-2 space-y-4 custom-scrollbar">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Nombre *</label>
            <input required type="text" name="nombre" value={formData.nombre} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all" placeholder="Ej. Juan" />
          </div>
          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Apellido *</label>
            <input required type="text" name="apellido" value={formData.apellido} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all" placeholder="Ej. Pérez" />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Cédula de Identidad</label>
          <input type="text" name="ci" value={formData.ci} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all" placeholder="Ej. 0912345678" />
        </div>

        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Síntomas / Motivo</label>
          <input type="text" name="enfermedad" value={formData.enfermedad} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all" placeholder="Ej. Dolor torácico" />
        </div>

        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Prioridad</label>
          <select name="triaje" value={formData.triaje} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm font-bold focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all cursor-pointer">
            <option value="Rojo">🔴 Rojo (Inmediato)</option>
            <option value="Amarillo">🟡 Amarillo (Urgente)</option>
            <option value="Verde">🟢 Verde (Ambulatorio)</option>
          </select>
        </div>

        <div className="border border-slate-200 rounded-2xl p-4 bg-slate-50/50 space-y-4">
          <div className="flex items-center gap-2">
            <ShieldCheck size={16} className="text-slate-400" />
            <span className="text-xs font-bold text-slate-700">Validación de Cobertura</span>
          </div>
          
          <label className="flex items-center gap-2 cursor-pointer group">
            <input type="checkbox" name="posee_seguro" checked={formData.posee_seguro} onChange={handleChange} className="w-4 h-4 text-rose-600 rounded border-slate-300 focus:ring-rose-500 transition-all" />
            <span className="text-[11px] font-bold text-slate-600 group-hover:text-slate-900 transition-colors">¿Paciente cuenta con seguro?</span>
          </label>

          {formData.posee_seguro && (
            <div className="space-y-1 animate-in fade-in slide-in-from-top-2 duration-300">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Póliza / Afiliación</label>
              <input type="text" name="numero_seguro" value={formData.numero_seguro} onChange={handleChange} className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2 text-sm focus:ring-4 focus:ring-rose-500/10 focus:border-rose-500 outline-none transition-all" placeholder="Ingrese número" />
            </div>
          )}
        </div>

        <button disabled={isSubmitting} type="submit" className="w-full bg-rose-600 hover:bg-rose-700 text-white font-black py-3 rounded-xl shadow-lg shadow-rose-500/30 transition-all active:scale-[0.98] flex items-center justify-center gap-2 mt-4 disabled:opacity-70 text-base uppercase tracking-widest">
          {isSubmitting ? (
            <Loader2 className="animate-spin" size={20} />
          ) : (
            <>
              Confirmar Ingreso
              <Send size={18} />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
