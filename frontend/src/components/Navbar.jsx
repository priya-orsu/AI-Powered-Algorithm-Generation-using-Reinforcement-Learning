import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, Search, LayoutDashboard, Shield, LogIn, LogOut, ChevronDown, User, Layers } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API } from '../services/api';

export function Navbar() {
    const { currentUser, isAdmin, isUser, logout } = useAuth();
    const location = useLocation();
    const [healthStatus, setHealthStatus] = useState('Checking');
    const [userDropdownOpen, setUserDropdownOpen] = useState(false);

    useEffect(() => {
        let isMounted = true;
        const checkHealth = async () => {
            try {
                const res = await API.getHealth();
                if (isMounted) setHealthStatus(res.status);
            } catch (err) {
                if (isMounted) setHealthStatus('Unhealthy');
            }
        };

        checkHealth();
        const interval = setInterval(checkHealth, 12000);
        return () => {
            isMounted = false;
            clearInterval(interval);
        };
    }, []);

    const isActive = (path) => location.pathname === path;

    return (
        <header className="sticky top-0 z-40 border-b border-white/5 bg-[#0d1322]/85 backdrop-blur-md">
            <div className="container mx-auto px-6 py-3.5 flex items-center justify-between">
                {/* Brand Logo */}
                <Link to="/" className="flex items-center gap-3 group">
                    <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-violet-600 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
                        <Brain className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-base font-extrabold text-white tracking-tight flex items-center gap-1.5">
                            AlgoGen <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-300 font-mono font-bold">Studio</span>
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono -mt-0.5">Hybrid GA-RL Synthesis</span>
                    </div>
                </Link>

                {/* Navigation Links */}
                <nav className="hidden md:flex items-center gap-6 text-xs font-semibold">
                    <Link
                        to="/"
                        className={`flex items-center gap-2 transition ${isActive('/') ? 'text-cyan-400 font-bold' : 'text-slate-400 hover:text-white'
                            }`}
                    >
                        <Search className="w-3.5 h-3.5" /> Studio Workbench
                    </Link>

                    <Link
                        to="/pipeline"
                        className={`flex items-center gap-2 transition ${isActive('/pipeline') ? 'text-cyan-400 font-bold' : 'text-slate-400 hover:text-white'
                            }`}
                    >
                        <Layers className="w-3.5 h-3.5" /> Real-World Solver
                    </Link>

                    {(isUser || isAdmin) && (
                        <Link
                            to="/dashboard"
                            className={`flex items-center gap-2 transition ${isActive('/dashboard') ? 'text-cyan-400 font-bold' : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            <LayoutDashboard className="w-3.5 h-3.5" /> Workspace
                        </Link>
                    )}

                    {isAdmin && (
                        <Link
                            to="/admin"
                            className={`flex items-center gap-2 transition ${isActive('/admin') ? 'text-cyan-400 font-bold' : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            <Shield className="w-3.5 h-3.5" /> Admin Console
                        </Link>
                    )}
                </nav>

                {/* Right Side Actions & User Menu */}
                <div className="flex items-center gap-4">

                    {!currentUser ? (
                        <Link
                            to="/login"
                            className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs transition shadow-md shadow-cyan-500/20 flex items-center gap-2"
                        >
                            <LogIn className="w-3.5 h-3.5" /> Sign In / Register
                        </Link>
                    ) : (
                        <div className="relative">
                            <button
                                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                                className="flex items-center gap-2.5 bg-slate-900 border border-white/10 hover:border-white/20 py-1.5 px-3 rounded-xl transition focus:outline-none"
                            >
                                <div className="w-6 h-6 rounded-lg bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-300 font-bold uppercase text-[11px]">
                                    {currentUser.username[0]}
                                </div>
                                <span className="text-xs font-semibold text-slate-200">{currentUser.username}</span>
                                <ChevronDown className="w-3 h-3 text-slate-400" />
                            </button>

                            {userDropdownOpen && (
                                <div
                                    onMouseLeave={() => setUserDropdownOpen(false)}
                                    className="absolute right-0 mt-2 w-48 rounded-xl bg-slate-900 border border-white/10 p-1.5 shadow-2xl z-50 text-xs"
                                >
                                    <div className="px-3 py-2 text-[11px] text-slate-400 border-b border-white/5 font-mono mb-1">
                                        Signed in as <strong className="block text-cyan-300 truncate">{currentUser.username}</strong>
                                    </div>
                                    <Link
                                        to="/dashboard"
                                        onClick={() => setUserDropdownOpen(false)}
                                        className="flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition"
                                    >
                                        <User className="w-3.5 h-3.5 text-slate-400" /> My Workspace
                                    </Link>
                                    {isAdmin && (
                                        <Link
                                            to="/admin"
                                            onClick={() => setUserDropdownOpen(false)}
                                            className="flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition"
                                        >
                                            <Shield className="w-3.5 h-3.5 text-slate-400" /> Admin Console
                                        </Link>
                                    )}
                                    <button
                                        onClick={logout}
                                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg font-semibold text-rose-400 hover:bg-rose-950/30 transition text-left"
                                    >
                                        <LogOut className="w-3.5 h-3.5" /> Sign Out
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}
