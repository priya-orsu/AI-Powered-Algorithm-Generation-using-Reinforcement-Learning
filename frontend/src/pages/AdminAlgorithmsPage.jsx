import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Database, Plus, Edit3, Trash2, RefreshCw, X, Shield, Users, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { API } from '../services/api';

export function AdminAlgorithmsPage() {
    const { isAdmin } = useAuth();
    const { showToast } = useToast();
    const navigate = useNavigate();

    const [stats, setStats] = useState(null);
    const [algorithms, setAlgorithms] = useState([]);
    const [filterQuery, setFilterQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');
    const [loading, setLoading] = useState(true);

    // Modal state
    const [showModal, setShowModal] = useState(false);
    const [editingAlgo, setEditingAlgo] = useState(null);
    const [modalForm, setModalForm] = useState({
        algorithm_name: '',
        category: 'Graph',
        description: '',
        problem_statement: '',
        pseudocode: '',
        best_case: 'O(1)',
        average_case: 'O(n)',
        worst_case: 'O(n^2)',
        space_complexity: 'O(n)'
    });

    useEffect(() => {
        if (!isAdmin) {
            navigate('/login?error=admin_required');
            return;
        }

        fetchAdminData();
    }, [isAdmin, navigate]);

    const fetchAdminData = async () => {
        setLoading(true);
        try {
            const statRes = await API.getBackendStatistics();
            setStats(statRes);

            const algosRes = await API.getAllAlgorithms();
            if (algosRes.status === 'success') {
                setAlgorithms(algosRes.data);
            }
        } catch (err) {
            showToast('Failed to load algorithm data: ' + err.message, 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleOpenCreateModal = () => {
        setEditingAlgo(null);
        setModalForm({
            algorithm_name: '',
            category: 'Graph',
            description: '',
            problem_statement: '',
            pseudocode: '',
            best_case: 'O(1)',
            average_case: 'O(n)',
            worst_case: 'O(n^2)',
            space_complexity: 'O(n)'
        });
        setShowModal(true);
    };

    const handleOpenEditModal = (algo) => {
        setEditingAlgo(algo);
        setModalForm({
            algorithm_name: algo.algorithm_name,
            category: algo.category || 'Graph',
            description: algo.description || '',
            problem_statement: algo.problem_statement || '',
            pseudocode: algo.pseudocode || '',
            best_case: typeof algo.time_complexity === 'object' ? algo.time_complexity.best : 'O(1)',
            average_case: typeof algo.time_complexity === 'object' ? algo.time_complexity.average : 'O(n)',
            worst_case: typeof algo.time_complexity === 'object' ? algo.time_complexity.worst : 'O(n^2)',
            space_complexity: algo.space_complexity || 'O(n)'
        });
        setShowModal(true);
    };

    const handleSaveAlgorithm = async (e) => {
        e.preventDefault();
        const payload = {
            algorithm_name: modalForm.algorithm_name.trim(),
            category: modalForm.category.trim(),
            description: modalForm.description.trim(),
            problem_statement: modalForm.problem_statement.trim(),
            pseudocode: modalForm.pseudocode,
            time_complexity: {
                best: modalForm.best_case,
                average: modalForm.average_case,
                worst: modalForm.worst_case
            },
            space_complexity: modalForm.space_complexity
        };

        try {
            if (editingAlgo) {
                await API.updateAlgorithm(editingAlgo.algorithm_name, payload);
                showToast(`Updated "${payload.algorithm_name}" in MongoDB!`, 'success');
            } else {
                await API.createAlgorithm(payload);
                showToast(`Created "${payload.algorithm_name}" in MongoDB!`, 'success');
            }
            setShowModal(false);
            fetchAdminData();
        } catch (err) {
            showToast(err.message || 'Operation failed', 'error');
        }
    };

    const handleDeleteAlgorithm = async (name) => {
        if (!window.confirm(`Are you sure you want to delete "${name}" from MongoDB?`)) return;

        try {
            await API.deleteAlgorithm(name);
            showToast(`Deleted "${name}" from MongoDB`, 'info');
            fetchAdminData();
        } catch (err) {
            showToast('Delete failed: ' + err.message, 'error');
        }
    };

    const categoriesList = ['All', ...new Set(algorithms.map((a) => a.category).filter(Boolean))];

    const filteredAlgorithms = algorithms.filter((algo) => {
        const matchesCategory = selectedCategory === 'All' || algo.category === selectedCategory;
        const matchesQuery =
            !filterQuery.trim() ||
            algo.algorithm_name.toLowerCase().includes(filterQuery.toLowerCase()) ||
            (algo.description && algo.description.toLowerCase().includes(filterQuery.toLowerCase()));
        return matchesCategory && matchesQuery;
    });

    return (
        <div className="container mx-auto px-4 py-8 max-w-7xl space-y-8">
            {/* Header Banner & Admin Section Tabs */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/5 pb-6">
                <div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-500/30 text-indigo-300 text-xs font-mono mb-2">
                        <Shield className="w-3.5 h-3.5 text-indigo-400" />
                        <span>Administrator Catalog Console</span>
                    </div>
                    <h1 className="text-2xl md:text-3xl font-extrabold text-white">MongoDB Algorithm Repository</h1>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={fetchAdminData}
                        className="px-3.5 py-2 bg-slate-900 border border-white/10 hover:border-white/20 text-slate-300 hover:text-white text-xs font-semibold rounded-xl transition flex items-center gap-1.5"
                    >
                        <RefreshCw className="w-3.5 h-3.5" /> Refresh List
                    </button>
                    <button
                        onClick={handleOpenCreateModal}
                        className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl transition flex items-center gap-2 shadow-md shadow-cyan-500/20"
                    >
                        <Plus className="w-4 h-4" /> Add New Algorithm
                    </button>
                </div>
            </div>

            {/* Admin Console Sub-Navigation Tabs */}
            <div className="flex border-b border-white/10 gap-4 text-xs font-bold">
                <Link
                    to="/admin"
                    className="py-2.5 px-4 text-slate-400 hover:text-white transition flex items-center gap-2"
                >
                    <Users className="w-4 h-4 text-slate-400" /> User Directory & Analytics
                </Link>
                <Link
                    to="/admin/algorithms"
                    className="py-2.5 px-4 border-b-2 border-cyan-400 text-cyan-300 bg-cyan-600/10 rounded-t-xl flex items-center gap-2"
                >
                    <Database className="w-4 h-4 text-cyan-400" /> Algorithm Catalog CRUD ({algorithms.length})
                </Link>
            </div>

            {/* Filter & Search Bar */}
            <div className="card-studio p-4 flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="relative flex-1 w-full flex items-center">
                    <Search className="w-4 h-4 text-slate-400 absolute left-3.5" />
                    <input
                        type="text"
                        value={filterQuery}
                        onChange={(e) => setFilterQuery(e.target.value)}
                        placeholder="Search algorithms by name or description..."
                        className="w-full bg-[#0d1322] border border-white/10 focus:border-cyan-400 rounded-xl py-2.5 pl-10 pr-4 text-xs font-medium text-white focus:outline-none focus:ring-1 focus:ring-cyan-500"
                    />
                </div>

                <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto">
                    {categoriesList.map((cat) => (
                        <button
                            key={cat}
                            onClick={() => setSelectedCategory(cat)}
                            className={`px-3 py-1.5 rounded-lg text-xs font-semibold shrink-0 transition ${
                                selectedCategory === cat
                                    ? 'bg-cyan-600 text-white shadow'
                                    : 'bg-slate-900 border border-white/10 text-slate-400 hover:text-white'
                            }`}
                        >
                            {cat}
                        </button>
                    ))}
                </div>
            </div>

            {/* CRUD Algorithms Table */}
            <div className="card-studio p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-white/5 pb-3">
                    <h2 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <Database className="w-4 h-4 text-cyan-400" /> Catalog Entries ({filteredAlgorithms.length} of {algorithms.length})
                    </h2>
                </div>

                {loading ? (
                    <div className="text-center py-12 text-slate-400 text-xs">Loading algorithm records...</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-xs">
                            <thead>
                                <tr className="border-b border-white/10 text-slate-400 font-mono text-[10px] uppercase">
                                    <th className="py-2.5 px-3">Algorithm Name</th>
                                    <th className="py-2.5 px-3">Category</th>
                                    <th className="py-2.5 px-3">Description</th>
                                    <th className="py-2.5 px-3 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {filteredAlgorithms.map((algo) => (
                                    <tr key={algo.algorithm_name} className="hover:bg-white/5 transition">
                                        <td className="py-3 px-3 font-bold text-white max-w-[180px] truncate">
                                            {algo.algorithm_name}
                                        </td>
                                        <td className="py-3 px-3">
                                            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-cyan-950 text-cyan-300 border border-cyan-800/40">
                                                {algo.category}
                                            </span>
                                        </td>
                                        <td className="py-3 px-3 text-slate-400 max-w-md truncate">{algo.description}</td>
                                        <td className="py-3 px-3 text-right space-x-2">
                                            <button
                                                onClick={() => handleOpenEditModal(algo)}
                                                className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition inline-flex items-center gap-1"
                                            >
                                                <Edit3 className="w-3 h-3" /> Edit
                                            </button>
                                            <button
                                                onClick={() => handleDeleteAlgorithm(algo.algorithm_name)}
                                                className="px-2.5 py-1 rounded bg-rose-950/60 hover:bg-rose-900 border border-rose-800/40 text-rose-300 text-[11px] font-medium transition inline-flex items-center gap-1"
                                            >
                                                <Trash2 className="w-3 h-3" /> Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Create / Edit Modal */}
            {showModal && (
                <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
                    <div className="card-studio w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 space-y-4">
                        <div className="flex items-center justify-between border-b border-white/10 pb-3">
                            <h3 className="text-sm font-bold text-white">
                                {editingAlgo ? `Edit "${editingAlgo.algorithm_name}"` : 'Add New Algorithm to MongoDB'}
                            </h3>
                            <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white">
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        <form onSubmit={handleSaveAlgorithm} className="space-y-4 text-xs">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-1">
                                    <label className="text-slate-300 font-semibold">Algorithm Name</label>
                                    <input
                                        type="text"
                                        value={modalForm.algorithm_name}
                                        onChange={(e) => setModalForm({ ...modalForm, algorithm_name: e.target.value })}
                                        required
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-xl p-2.5 text-white"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-slate-300 font-semibold">Category</label>
                                    <input
                                        type="text"
                                        value={modalForm.category}
                                        onChange={(e) => setModalForm({ ...modalForm, category: e.target.value })}
                                        required
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-xl p-2.5 text-white"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1">
                                <label className="text-slate-300 font-semibold">Description</label>
                                <textarea
                                    value={modalForm.description}
                                    onChange={(e) => setModalForm({ ...modalForm, description: e.target.value })}
                                    rows={3}
                                    required
                                    className="w-full bg-[#0d1322] border border-white/10 rounded-xl p-2.5 text-white"
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="text-slate-300 font-semibold">Problem Statement</label>
                                <textarea
                                    value={modalForm.problem_statement}
                                    onChange={(e) => setModalForm({ ...modalForm, problem_statement: e.target.value })}
                                    rows={2}
                                    className="w-full bg-[#0d1322] border border-white/10 rounded-xl p-2.5 text-white"
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="text-slate-300 font-semibold">Pseudocode</label>
                                <textarea
                                    value={modalForm.pseudocode}
                                    onChange={(e) => setModalForm({ ...modalForm, pseudocode: e.target.value })}
                                    rows={5}
                                    className="w-full bg-[#080c14] border border-white/10 rounded-xl p-2.5 font-mono text-cyan-300"
                                />
                            </div>

                            <div className="grid grid-cols-4 gap-2">
                                <div className="space-y-1">
                                    <label className="text-[10px] text-slate-400 uppercase font-mono">Best Time</label>
                                    <input
                                        type="text"
                                        value={modalForm.best_case}
                                        onChange={(e) => setModalForm({ ...modalForm, best_case: e.target.value })}
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-lg p-2 font-mono text-emerald-400"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] text-slate-400 uppercase font-mono">Avg Time</label>
                                    <input
                                        type="text"
                                        value={modalForm.average_case}
                                        onChange={(e) => setModalForm({ ...modalForm, average_case: e.target.value })}
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-lg p-2 font-mono text-cyan-400"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] text-slate-400 uppercase font-mono">Worst Time</label>
                                    <input
                                        type="text"
                                        value={modalForm.worst_case}
                                        onChange={(e) => setModalForm({ ...modalForm, worst_case: e.target.value })}
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-lg p-2 font-mono text-rose-400"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] text-slate-400 uppercase font-mono">Space</label>
                                    <input
                                        type="text"
                                        value={modalForm.space_complexity}
                                        onChange={(e) => setModalForm({ ...modalForm, space_complexity: e.target.value })}
                                        className="w-full bg-[#0d1322] border border-white/10 rounded-lg p-2 font-mono text-violet-400"
                                    />
                                </div>
                            </div>

                            <div className="flex justify-end gap-2 pt-3 border-t border-white/10">
                                <button
                                    type="button"
                                    onClick={() => setShowModal(false)}
                                    className="px-4 py-2 rounded-xl border border-white/10 text-slate-300 hover:bg-white/5 font-semibold"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-5 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold shadow-md shadow-cyan-600/20"
                                >
                                    Save Record
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
