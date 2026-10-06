import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { UserHistoryProvider } from './context/UserHistoryContext';
import { ToastProvider } from './context/ToastContext';
import { Navbar } from './components/Navbar';
import { StudioPage } from './pages/StudioPage';
import { LoginPage } from './pages/LoginPage';
import { UserDashboardPage } from './pages/UserDashboardPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AdminAlgorithmsPage } from './pages/AdminAlgorithmsPage';
import { PipelineExplainerPage } from './pages/PipelineExplainerPage';
import StarfieldGravity from './components/StarfieldGravity';

// Route guards
function ProtectedRoute({ children }) {
    const { isUser, isAdmin } = useAuth();
    if (!isUser && !isAdmin) {
        return <Navigate to="/login" replace />;
    }
    return children;
}

function PublicOnlyRoute({ children }) {
    const { isUser, isAdmin } = useAuth();
    if (isUser || isAdmin) {
        return <Navigate to="/" replace />;
    }
    return children;
}

function AdminRoute({ children }) {
    const { isAdmin } = useAuth();
    if (!isAdmin) {
        return <Navigate to="/login?error=admin_required" replace />;
    }
    return children;
}

export default function App() {
    return (
        <AuthProvider>
            <UserHistoryProvider>
                <ToastProvider>
                    <div className="app-shell min-h-screen flex flex-col text-slate-100 selection:bg-cyan-500 selection:text-white">
                        <StarfieldGravity
                            starCount={200}
                            gravityRadius={180}
                            gravityStrength={0.9}
                            constellationDistance={110}
                            speedMultiplier={0.5}
                            colors={["#06b6d4", "#8b5cf6", "#3b82f6", "#ec4899", "#ffffff"]}
                        />
                        <div className="app-content min-h-screen flex flex-col">
                        <Navbar />
                        <main className="flex-1">
                            <Routes>
                                {/* Default route: protected Studio Workbench */}
                                <Route
                                    path="/"
                                    element={
                                        <ProtectedRoute>
                                            <StudioPage />
                                        </ProtectedRoute>
                                    }
                                />
                                {/* Login / Register page: shown first to unauthenticated users */}
                                <Route
                                    path="/login"
                                    element={
                                        <PublicOnlyRoute>
                                            <LoginPage />
                                        </PublicOnlyRoute>
                                    }
                                />
                                <Route
                                    path="/pipeline"
                                    element={
                                        <ProtectedRoute>
                                            <PipelineExplainerPage />
                                        </ProtectedRoute>
                                    }
                                />
                                {/* User Dashboard: protected */}
                                <Route
                                    path="/dashboard"
                                    element={
                                        <ProtectedRoute>
                                            <UserDashboardPage />
                                        </ProtectedRoute>
                                    }
                                />
                                {/* Admin Console: protected for admins */}
                                <Route
                                    path="/admin"
                                    element={
                                        <AdminRoute>
                                            <AdminDashboardPage />
                                        </AdminRoute>
                                    }
                                />
                                <Route
                                    path="/admin/algorithms"
                                    element={
                                        <AdminRoute>
                                            <AdminAlgorithmsPage />
                                        </AdminRoute>
                                    }
                                />
                                {/* Fallback route */}
                                <Route path="*" element={<Navigate to="/" replace />} />
                            </Routes>
                        </main>
                        <footer className="border-t border-white/5 py-6 bg-[#0d1322]/80 text-center text-xs text-slate-500 font-mono">
                            AlgoGen Studio • Hybrid GA-RL Algorithm Generation Engine • Powered by FastAPI & MongoDB
                        </footer>
                        </div>
                    </div>
                </ToastProvider>
            </UserHistoryProvider>
        </AuthProvider>
    );
}
