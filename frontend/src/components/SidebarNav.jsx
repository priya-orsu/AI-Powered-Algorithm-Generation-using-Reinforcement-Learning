import React from 'react';
import { 
    Star, 
    ChevronRight, 
    Cpu
} from 'lucide-react';
import { useUserHistory } from '../context/UserHistoryContext';

export function SidebarNav({ onSelectAlgorithm }) {
    const { bookmarks } = useUserHistory();

    return (
        <aside className="w-full space-y-6">
            {/* GA-RL Status Card */}
            <div className="p-4 rounded-2xl bg-gradient-to-b from-slate-900/90 to-cyan-950/40 border border-cyan-500/20 backdrop-blur-md shadow-lg shadow-cyan-950/30 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />
                <div className="flex items-center gap-2.5 mb-2">
                    <div className="w-7 h-7 rounded-lg bg-cyan-500/20 border border-cyan-400/30 flex items-center justify-center text-cyan-300">
                        <Cpu className="w-4 h-4 animate-pulse text-cyan-400" />
                    </div>
                    <div>
                        <h4 className="text-xs font-bold text-white tracking-wide">GA-RL Hybrid Engine</h4>
                        <span className="text-[10px] text-cyan-400 font-mono font-semibold">Q-Learning + GA Active</span>
                    </div>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed mb-3">
                    Synthesizing evolutionary parameters with target accuracy <span className="text-emerald-400 font-bold font-mono">≥98%</span>.
                </p>
                <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono pt-2 border-t border-white/5">
                    <span>Cache Latency: <strong className="text-cyan-300">&lt; 15ms</strong></span>
                    <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-bold">Online</span>
                </div>
            </div>

            {/* Saved Bookmarks */}
            {bookmarks && bookmarks.length > 0 && (
                <div className="p-4 rounded-2xl bg-slate-900/80 border border-white/5 backdrop-blur-md">
                    <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                        <Star className="w-3.5 h-3.5 text-yellow-400 fill-yellow-400/20" /> Saved Bookmarks
                    </h3>
                    <div className="space-y-1.5">
                        {bookmarks.slice(0, 5).map((bName, idx) => (
                            <button
                                key={idx}
                                onClick={() => onSelectAlgorithm && onSelectAlgorithm(bName)}
                                className="w-full flex items-center justify-between p-2 rounded-xl bg-slate-950/40 hover:bg-slate-800/60 border border-white/5 hover:border-yellow-500/30 transition group text-left"
                            >
                                <div className="flex items-center gap-2 overflow-hidden">
                                    <Star className="w-3 h-3 text-yellow-400 shrink-0 fill-yellow-400" />
                                    <span className="text-xs font-medium text-slate-300 group-hover:text-yellow-200 transition truncate">
                                        {bName}
                                    </span>
                                </div>
                                <ChevronRight className="w-3 h-3 text-slate-600 group-hover:text-yellow-400 transition" />
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </aside>
    );
}

export default SidebarNav;
