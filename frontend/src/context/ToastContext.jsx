import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle2, AlertTriangle, Info, X } from 'lucide-react';

const ToastContext = createContext();

export function ToastProvider({ children }) {
    const [toasts, setToasts] = useState([]);

    const showToast = useCallback((message, type = 'success', duration = 4000) => {
        const id = Date.now() + Math.random().toString(36).substring(2, 9);
        setToasts((prev) => [...prev, { id, message, type, duration }]);

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

            {/* ── Keyframe animations ── */}
            <style>{`
                @keyframes toast-slide-down {
                    from { opacity: 0; transform: translateY(-32px) scale(0.94); }
                    to   { opacity: 1; transform: translateY(0px)   scale(1);    }
                }
                @keyframes toast-progress {
                    from { width: 100%; }
                    to   { width: 0%;   }
                }
                .toast-enter {
                    animation: toast-slide-down 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
                }
                .toast-bar {
                    animation: toast-progress linear both;
                }
            `}</style>

            {/* ── Toast Container — fixed top-center ── */}
            <div
                style={{ top: '76px', left: '50%', transform: 'translateX(-50%)' }}
                className="fixed z-[9999] flex flex-col items-center gap-3 w-full max-w-xl pointer-events-none px-4"
            >
                {toasts.map((toast) => {
                    const isSuccess = toast.type === 'success';
                    const isError   = toast.type === 'error';
                    const isInfo    = !isSuccess && !isError;

                    const colors = isSuccess
                        ? {
                            wrap:      'bg-emerald-950/95 border-emerald-400/70',
                            glow:      '0 0 32px 6px rgba(52,211,153,0.40), 0 4px 24px rgba(0,0,0,0.6)',
                            iconWrap:  'bg-emerald-500/25 text-emerald-300',
                            text:      'text-emerald-100',
                            bar:       'bg-emerald-400',
                          }
                        : isError
                        ? {
                            wrap:      'bg-rose-950/95 border-rose-400/70',
                            glow:      '0 0 32px 6px rgba(251,113,133,0.40), 0 4px 24px rgba(0,0,0,0.6)',
                            iconWrap:  'bg-rose-500/25 text-rose-300',
                            text:      'text-rose-100',
                            bar:       'bg-rose-400',
                          }
                        : {
                            wrap:      'bg-cyan-950/95 border-cyan-400/70',
                            glow:      '0 0 32px 6px rgba(34,211,238,0.40), 0 4px 24px rgba(0,0,0,0.6)',
                            iconWrap:  'bg-cyan-500/25 text-cyan-300',
                            text:      'text-cyan-100',
                            bar:       'bg-cyan-400',
                          };

                    return (
                        <div
                            key={toast.id}
                            className={`toast-enter w-full pointer-events-auto rounded-2xl border-2 backdrop-blur-xl overflow-hidden ${colors.wrap}`}
                            style={{ boxShadow: colors.glow }}
                        >
                            {/* Content row */}
                            <div className="flex items-center gap-4 px-5 py-4">
                                {/* Icon badge */}
                                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${colors.iconWrap}`}>
                                    {isSuccess && <CheckCircle2 className="w-6 h-6" />}
                                    {isError   && <AlertTriangle className="w-6 h-6" />}
                                    {isInfo    && <Info className="w-6 h-6" />}
                                </div>

                                {/* Message */}
                                <p className={`flex-1 text-sm font-semibold leading-snug tracking-wide ${colors.text}`}>
                                    {toast.message}
                                </p>

                                {/* Close */}
                                <button
                                    onClick={() => removeToast(toast.id)}
                                    className="text-slate-400 hover:text-white transition-colors shrink-0 ml-1"
                                    aria-label="Dismiss"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>

                            {/* Auto-dismiss progress bar */}
                            <div className="h-[3px] w-full bg-white/10">
                                <div
                                    className={`h-full toast-bar ${colors.bar}`}
                                    style={{ animationDuration: `${toast.duration ?? 4000}ms` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        </ToastContext.Provider>
    );
}

export function useToast() {
    return useContext(ToastContext);
}
