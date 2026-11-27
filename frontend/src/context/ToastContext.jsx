import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle2, AlertTriangle, Info, X } from 'lucide-react';

const ToastContext = createContext();

export function ToastProvider({ children }) {
    const [toasts, setToasts] = useState([]);

    const showToast = useCallback((message, type = 'success', duration = 4000) => {
        const id = Date.now() + Math.random().toString(36).substring(2, 9);
        setToasts((prev) => [...prev, { id, message, type }]);

        setTimeout(() => {
            setToasts((prev) => prev.filter((t) => t.id !== id));
        }, duration);
    }, []);

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ showToast, removeToast }}>
            {children}
            {/* Toast Container */}
            <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-3 max-w-md w-full pointer-events-none">
                {toasts.map((toast) => (
                    <div
                        key={toast.id}
                        className={`toast-slide-in p-4 rounded-xl shadow-xl flex items-center gap-3 backdrop-blur-md pointer-events-auto border ${
                            toast.type === 'success'
                                ? 'bg-emerald-950/90 border-emerald-500/30 text-emerald-200'
                                : toast.type === 'error'
                                ? 'bg-rose-950/90 border-rose-500/30 text-rose-200'
                                : 'bg-cyan-950/90 border-cyan-500/30 text-cyan-200'
                        }`}
                    >
                        <div
                            className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                                toast.type === 'success'
                                    ? 'bg-emerald-500/20 text-emerald-400'
                                    : toast.type === 'error'
                                    ? 'bg-rose-500/20 text-rose-400'
                                    : 'bg-cyan-500/20 text-cyan-400'
                            }`}
                        >
                            {toast.type === 'success' && <CheckCircle2 className="w-4 h-4" />}
                            {toast.type === 'error' && <AlertTriangle className="w-4 h-4" />}
                            {toast.type === 'info' && <Info className="w-4 h-4" />}
                        </div>
                        <div className="flex-1 text-xs font-medium">{toast.message}</div>
                        <button
                            onClick={() => removeToast(toast.id)}
                            className="text-slate-400 hover:text-white transition"
                        >
                            <X className="w-3.5 h-3.5" />
                        </button>
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
}

export function useToast() {
    return useContext(ToastContext);
}
