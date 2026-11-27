import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, Database, RefreshCw, Users, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { API } from '../services/api';

export function AdminDashboardPage() {
    const { isAdmin } = useAuth();
    const { showToast } = useToast();
    const navigate = useNavigate();

    const [stats, setStats] = useState(null);
    const [userDirectory, setUserDirectory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!isAdmin) {
            navigate('/login?error=admin_required');
            return;
        }

        fetchAdminData();
    }, [isAdmin, navigate]);

    const loadUsersAnalytics = () => {
        const registered = JSON.parse(localStorage.getItem('simulated_registered_users') || '[]');
        const allUsersMap = new Map();

        allUsersMap.set('admin', { username: 'admin', email: 'admin@example.com', role: 'Administrator' });
        allUsersMap.set('user', { username: 'user', email: 'user@example.com', role: 'Standard User' });

        registered.forEach((u) => {
            allUsersMap.set(u.username.toLowerCase(), {
                username: u.username,
                email: u.email,
                role: u.username.toLowerCase() === 'admin' ? 'Administrator' : 'Standard User'
            });
        });

        const list = [];
        allUsersMap.forEach((user, key) => {
            const historyKey = `user_search_history_${key}`;
            const history = JSON.parse(localStorage.getItem(historyKey) || '[]');
            list.push({
                ...user,
                searchCount: history.length,
                lastSearch: history.length > 0 ? history[0].timestamp : null
            });
        });

        setUserDirectory(list);
    };

    const fetchAdminData = async () => {
        setLoading(true);
        loadUsersAnalytics();

        try {
            const statRes = await API.getBackendStatistics();
            setStats(statRes);
        } catch (err) {
            showToast('Failed to load admin metrics: ' + err.message, 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8 max-w-7xl space-y-8">
            {/* Header Banner */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/5 pb-6">
                <div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-500/30 text-indigo-300 text-xs font-mono mb-2">
                        <Shield className="w-3.5 h-3.5 text-indigo-400" />
                        <span>Administrator Analytics Console</span>
                    </div>
                    <h1 className="text-2xl md:text-3xl font-extrabold text-white">System Health & User Search Analytics</h1>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={fetchAdminData}
                        className="px-3.5 py-2 bg-slate-900 border border-white/10 hover:border-white/20 text-slate-300 hover:text-white text-xs font-semibold rounded-xl transition flex items-center gap-1.5"
                    >
                        <RefreshCw className="w-3.5 h-3.5" /> Refresh Analytics
                    </button>
                    <Link
                        to="/admin/algorithms"
                        className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl transition flex items-center gap-2 shadow-md shadow-cyan-500/20"
                    >
                        <Database className="w-4 h-4" /> Manage Algorithms Catalog
                    </Link>
                </div>
            </div>

            {/* Admin Console Sub-Navigation Tabs */}
            <div className="flex border-b border-white/10 gap-4 text-xs font-bold">
                <Link
                    to="/admin"
                    className="py-2.5 px-4 border-b-2 border-cyan-400 text-cyan-300 bg-cyan-600/10 rounded-t-xl flex items-center gap-2"
                >
                    <Users className="w-4 h-4 text-cyan-400" /> User Directory & Analytics ({userDirectory.length})
                </Link>
                <Link
                    to="/admin/algorithms"
                    className="py-2.5 px-4 text-slate-400 hover:text-white transition flex items-center gap-2"
                >
                    <Database className="w-4 h-4 text-slate-400" /> Algorithm Catalog CRUD Manager
                </Link>
            </div>

            {/* Stats Bar */}
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <div className="card-studio p-5 space-y-1">
                    <span className="text-xs text-slate-400">Total MongoDB Algorithms</span>
                    <div className="text-2xl font-extrabold text-white font-mono">{stats?.total_algorithms || '12'}</div>
                </div>
                <div className="card-studio p-5 space-y-1">
                    <span className="text-xs text-slate-400">System Registered Users</span>
                    <div className="text-2xl font-extrabold text-cyan-400 font-mono">{userDirectory.length}</div>
                </div>
                <div className="card-studio p-5 space-y-1">
                    <span className="text-xs text-slate-400">MongoDB Health Status</span>
                    <div className="text-xl font-bold text-emerald-400 capitalize">{stats?.database_status || 'Connected'}</div>
                </div>
                <div className="card-studio p-5 space-y-1">
                    <span className="text-xs text-slate-400">Synthesis Engine</span>
                    <div className="text-xl font-bold text-indigo-400">GA-RL Active</div>
                </div>
            </div>

            {/* User Directory & Search Activity Table */}
            <div className="card-studio p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-white/5 pb-3">
                    <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <Users className="w-4 h-4 text-cyan-400" /> User Directory & Search Query Analytics ({userDirectory.length} Accounts)
                    </h2>
                </div>

                {loading ? (
                    <div className="text-center py-12 text-slate-400 text-xs">Loading user analytics...</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-xs">
                            <thead>
                                <tr className="border-b border-white/10 text-slate-400 font-mono text-[10px] uppercase">
                                    <th className="py-2.5 px-3">User Account</th>
                                    <th className="py-2.5 px-3">Email Address</th>
                                    <th className="py-2.5 px-3">Account Role</th>
                                    <th className="py-2.5 px-3">Total Searches Performed</th>
                                    <th className="py-2.5 px-3 text-right">Last Search Activity</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {userDirectory.map((user) => (
                                    <tr key={user.username} className="hover:bg-white/5 transition">
                                        <td className="py-3 px-3">
                                            <div className="flex items-center gap-2.5">
                                                <div className="w-7 h-7 rounded-lg bg-cyan-950 border border-cyan-500/30 text-cyan-300 font-bold flex items-center justify-center text-xs uppercase">
                                                    {user.username[0]}
                                                </div>
                                                <span className="font-bold text-white">{user.username}</span>
                                            </div>
                                        </td>
                                        <td className="py-3 px-3 text-slate-300 font-mono">{user.email}</td>
                                        <td className="py-3 px-3">
                                            <span
                                                className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                                                    user.role === 'Administrator'
                                                        ? 'bg-indigo-950 text-indigo-300 border-indigo-800/40'
                                                        : 'bg-slate-900 text-slate-300 border-white/10'
                                                }`}
                                            >
                                                {user.role}
                                            </span>
                                        </td>
                                        <td className="py-3 px-3">
                                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800/40 font-mono font-bold text-xs">
                                                <Search className="w-3 h-3 text-cyan-400" /> {user.searchCount} searches
                                            </span>
                                        </td>
                                        <td className="py-3 px-3 text-right text-slate-400 font-mono text-[11px]">
                                            {user.lastSearch ? new Date(user.lastSearch).toLocaleString() : 'No activity logged'}
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
