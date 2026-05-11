"use client";

import { useState, useEffect } from "react";
import { Send, AlertTriangle, ShieldCheck, Loader2, ClipboardCheck, CheckCircle } from "lucide-react";

export default function EmergencyForm() {
  interface FormData {
    nombre: string;
    apellido: string;
    ci: string;
    posee_seguro: boolean;
    numero_seguro: string;
  }

  const [formData, setFormData] = useState<FormData>({
    nombre: "",
    apellido: "",
    ci: "",
    posee_seguro: false,
    numero_seguro: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSearchingCi, setIsSearchingCi] = useState(false);
  const [patientFound, setPatientFound] = useState(false);

  // Autocomplete logic for cédula
  useEffect(() => {
    const searchPatientByCi = async (ci: string) => {
      if (!ci || ci.length !== 10) return;
      
      setIsSearchingCi(true);
      try {
        const response = await fetch(`http://localhost:8000/patients/${ci}`);
        if (response.ok) {
          const patientData = await response.json();
          setFormData(prev => ({
            ...prev,
            nombre: patientData.nombre || '',
            numero_seguro: patientData.numero_seguro || ''
          }));
          setPatientFound(true);
        } else {
          // Check for test users if not found in backend
          const testUsers = {
            '1726354910': { nombre: 'Juan Pérez', numero_seguro: 'SEG-987654' },
            '0912345678': { nombre: 'María García', numero_seguro: 'SEG-123456' },
            '1711223344': { nombre: 'Carlos Rodríguez', numero_seguro: 'SEG-555666' }
          };
          
          if (testUsers[ci as keyof typeof testUsers]) {
            const testUser = testUsers[ci as keyof typeof testUsers];
            setFormData(prev => ({
              ...prev,
              nombre: testUser.nombre,
              numero_seguro: testUser.numero_seguro
            }));
            setPatientFound(true);
          } else {
            setPatientFound(false);
          }
        }
      } catch (error) {
        console.error("Error searching patient:", error);
      } finally {
        setIsSearchingCi(false);
      }
    };

    const timeoutId = setTimeout(searchPatientByCi, 500);
    return () => clearTimeout(timeoutId);
  }, [formData.ci]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const formStr = `[FORMULARIO DE INGRESO]
Nombre: ${formData.nombre}
C.I: ${formData.ci || 'No proporcionado'}
Seguro: ${formData.posee_seguro ? "Sí (Póliza: " + formData.numero_seguro + ")" : "No"}`;

      const event = new CustomEvent('sentinel-form-submit', { 
        detail: { 
          text: formStr, 
          formData: formData 
        } 
      });
      window.dispatchEvent(event);
      
      // Limpiar un poco el formulario
      setFormData(prev => ({...prev, ci: "", numero_seguro: ""}));
      setPatientFound(false);
      
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
    
    // Reset patient found status if CI changes
    if (name === 'ci') {
      setPatientFound(false);
    }
  };

  return (
    <div className="bg-white/30 backdrop-blur-2xl border border-white/10 rounded-[2rem] flex flex-col h-full min-h-0 overflow-hidden border-t-2 border-t-cyan-400/30 p-6 shadow-xl shadow-slate-200/50">
      <div className="flex items-center gap-2 mb-3 border-b border-white/10 pb-3">
        <div className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center">
          <ClipboardCheck size={16} className="text-emerald-400" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-slate-800 tracking-tight">Registro de Admisión</h2>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto pr-1 space-y-3 scrollbar-thin scrollbar-track-slate-800/20 scrollbar-thumb-cyan-500/30 hover:scrollbar-thumb-cyan-500/50">
        <div className="grid grid-cols-2 gap-2">
          <div className="space-y-1">
            <label className="text-[9px] font-bold text-cyan-700/80 uppercase tracking-wider">Cédula *</label>
            <div className="relative">
              <input 
                type="text" 
                name="ci" 
                value={formData.ci} 
                onChange={handleChange} 
                className="w-full bg-white/80 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400/30 focus:border-cyan-400 focus:border-b-2 focus:border-b-cyan-400 outline-none transition-all backdrop-blur-sm" 
                placeholder="Ingrese cédula de 10 dígitos" 
                maxLength={10}
              />
              {isSearchingCi && (
                <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                  <Loader2 className="animate-spin text-cyan-400" size={14} />
                </div>
              )}
            </div>
            {patientFound && (
              <p className="text-xs text-emerald-400 font-medium">✓ Paciente encontrado</p>
            )}
          </div>
          
          <div className="space-y-1">
            <label className="text-[9px] font-bold text-cyan-700/80 uppercase tracking-wider">Número de Seguro</label>
            <div className="relative">
              <input 
                type="text" 
                name="numero_seguro" 
                value={formData.numero_seguro} 
                onChange={handleChange} 
                className="w-full bg-white/80 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400/30 focus:border-cyan-400 focus:border-b-2 focus:border-b-cyan-400 outline-none transition-all backdrop-blur-sm" 
                placeholder="Número de póliza" 
                readOnly={patientFound}
              />
              {patientFound && (
                <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                  <CheckCircle className="text-emerald-400" size={14} />
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-[9px] font-bold text-cyan-700/80 uppercase tracking-wider">Nombre Completo *</label>
          <div className="relative">
            <input 
              required 
              type="text" 
              name="nombre" 
              value={formData.nombre} 
              onChange={handleChange} 
              readOnly={patientFound}
              className={`w-full bg-white/80 border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400/30 focus:border-cyan-400 focus:border-b-2 focus:border-b-cyan-400 outline-none transition-all backdrop-blur-sm ${patientFound ? 'bg-slate-100/60 cursor-not-allowed' : ''}`} 
              placeholder="Nombre Completo" 
            />
            {patientFound && (
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                <CheckCircle className="text-emerald-400" size={14} />
              </div>
            )}
          </div>
        </div>

        <button disabled={isSubmitting || isSearchingCi || !patientFound || !formData.nombre} type="submit" className="w-full bg-gradient-to-r from-cyan-400 to-emerald-400 hover:brightness-110 transition-all text-white font-black py-3 rounded-full active:scale-[0.98] flex items-center justify-center gap-2 mt-6 disabled:opacity-70 text-sm uppercase tracking-widest">
          {isSubmitting ? (
            <Loader2 className="animate-spin" size={16} />
          ) : (
            <>
              ADMITIR PACIENTE
              <Send size={14} />
            </>
          )}
        </button>
      </form>
    </div>
  );
}