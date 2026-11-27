import React from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Star, Clock, Trash2, ArrowRight, ShieldCheck, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useUserHistory } from '../context/UserHistoryContext';
import { useToast } from '../context/ToastContext';

export function UserDashboardPage() {
    const { currentUser, isAdmin } = useAuth();
    const { history, bookmarks, clearHistory, toggleBookmark } = useUserHistory();
    const { showToast } = useToast();
    const navigate = useNavigate();

    const handleSearchClick = (query) => {
        navigate(`/?query=${encodeURIComponent(query)}`);
    };

    const handleRemoveBookmark = (name, e) => {
        e.stopPropagation();
        toggleBookmark(name);
        showToast(`Removed "${name}" from bookmarks`, 'info');
    };

    const handleClearHistoryClick = () => {
        clearHistory();
        showToast('Search history cleared for your account', 'info');
    };

    return (
        <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
            {/* Header Banner */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/5 pb-6">
                <div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-300 text-xs font-mono mb-2">
                        <User className="w-3.5 h-3.5 text-cyan-400" />
                        <span>User Account Workspace</span>
                    </div>
                    <h1 className="text-2xl md:text-3xl font-extrabold text-white">
                        Welcome back, <span className="text-cyan-400">{currentUser?.username || 'Developer'}</span>
                    </h1>
                    <p className="text-slate-400 text-xs mt-1">Manage your bookmarked algorithms and isolated account search history.</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={() => navigate('/')}
                        className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl transition flex items-center gap-2 shadow-md shadow-cyan-500/20"
                    >
                        <Search className="w-3.5 h-3.5" /> Studio Workbench
                    </button>
                </div>
            </div>

            {/* Stats Overview Row */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="card-studio p-5 space-y-1">
                    <div className="flex justify-between items-center text-slate-400 text-xs">
                        <span>Account Search Logs</span>
                        <Clock className="w-4 h-4 text-cyan-400" />
                    </div>
                    <div className="text-2xl font-extrabold text-white font-mono">{history.length}</div>
                    <span className="text-[10px] text-slate-500 font-mono">Isolated for {currentUser?.username}</span>
                </div>

                <div className="card-studio p-5 space-y-1">
                    <div className="flex justify-between items-center text-slate-400 text-xs">
                        <span>Bookmarked Items</span>
                        <Star className="w-4 h-4 text-amber-400 fill-amber-400/20" />
                    </div>
                    <div className="text-2xl font-extrabold text-white font-mono">{bookmarks.length}</div>
                    <span className="text-[10px] text-slate-500 font-mono">Saved specifications</span>
                </div>

                <div className="card-studio p-5 space-y-1">
                    <div className="flex justify-between items-center text-slate-400 text-xs">
                        <span>Account Role</span>
                        <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    </div>
                    <div className="text-xl font-bold text-emerald-400 capitalize">{isAdmin ? 'Administrator' : 'Standard User'}</div>
                    <span className="text-[10px] text-slate-500 font-mono">Session active</span>
                </div>
            </div>

            {/* Bookmarked Algorithms Grid */}
            <div className="card-studio p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-white/5 pb-3">
                    <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <Star className="w-4 h-4 text-amber-400 fill-amber-400/20" /> My Bookmarked Algorithms ({bookmarks.length})
                    </h2>
                </div>

                {bookmarks.length === 0 ? (
                    <div className="text-center py-8 text-slate-500 text-xs space-y-2">
                        <p>No algorithms bookmarked yet.</p>
                        <button onClick={() => navigate('/')} className="text-cyan-400 hover:underline font-semibold">
                            Explore algorithms in Studio Workbench →
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        {bookmarks.map((name) => (
                            <div
                                key={name}
                                onClick={() => handleSearchClick(name)}
                                className="p-4 rounded-xl bg-dark-900 border border-white/10 hover:border-amber-500/40 cursor-pointer transition space-y-3 flex flex-col justify-between group"
                            >
                                <div className="flex justify-between items-start">
                                    <h3 className="text-sm font-bold text-white group-hover:text-amber-300 transition truncate pr-2">
                                        {name}
                                    </h3>
                                    <button
                                        onClick={(e) => handleRemoveBookmark(name, e)}
                                        className="text-slate-500 hover:text-rose-400 transition"
                                    >
                                        <Trash2 className="w-3.5 h-3.5" />
                                    </button>
                                </div>
                                <div className="flex items-center justify-between text-[10px] text-cyan-400 font-mono font-semibold pt-2 border-t border-white/5">
                                    <span>View Specification</span>
                                    <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Isolated Account History Table */}
            <div className="card-studio p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-white/5 pb-3">
                    <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <Clock className="w-4 h-4 text-cyan-400" /> Account Search History
                    </h2>
                    {history.length > 0 && (
                        <button
                            onClick={handleClearHistoryClick}
                            className="text-xs text-rose-400 hover:text-rose-300 transition flex items-center gap-1"
                        >
                            <Trash2 className="w-3.5 h-3.5" /> Clear History
                        </button>
                    )}
                </div>

                {history.length === 0 ? (
                    <p className="text-slate-500 text-xs text-center py-6">Your search activity will appear here.</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-xs">
                            <thead>
                                <tr className="border-b border-white/10 text-slate-400 font-mono text-[10px] uppercase">
                                    <th className="py-2.5 px-3">Search Query</th>
                                    <th className="py-2.5 px-3">Query Type</th>
                                    <th className="py-2.5 px-3">Result Status</th>
                                    <th className="py-2.5 px-3">Timestamp</th>
                                    <th className="py-2.5 px-3 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {history.map((item, idx) => (
                                    <tr key={idx} className="hover:bg-white/5 transition">
                                        <td className="py-3 px-3 font-bold text-white">{item.query}</td>
                                        <td className="py-3 px-3 text-slate-300 font-mono text-[11px]">{item.type}</td>
                                        <td className="py-3 px-3">
                                            <span
                                                className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                                                    item.status === 'Found' || (item.status && item.status.toLowerCase().includes('generated'))
                                                        ? 'bg-emerald-950 text-emerald-300 border-emerald-800/40'
                                                        : 'bg-rose-950 text-rose-300 border-rose-800/40'
                                                }`}
                                            >
                                                {item.status}
                                            </span>
                                        </td>
                                        <td className="py-3 px-3 text-slate-400 font-mono text-[11px]">
                                            {new Date(item.timestamp).toLocaleString()}
                                        </td>
                                        <td className="py-3 px-3 text-right">
                                            <button
                                                onClick={() => handleSearchClick(item.query)}
                                                className="text-cyan-400 hover:underline font-medium text-xs"
                                            >
                                                Re-run Search
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
