import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Brain, Lock, User, Mail, Eye, EyeOff, Shield, ArrowRight, CheckCircle2, ArrowLeft, X, KeyRound, RefreshCw, Sparkles, Send, AlertTriangle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { API } from '../services/api';

export function LoginPage() {
    const { loginAdmin, loginUser } = useAuth();
    const { showToast } = useToast();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    const [tab, setTab] = useState('login');
    const [loading, setLoading] = useState(false);

    // Passwords show/hide state
    const [showLoginPassword, setShowLoginPassword] = useState(false);
    const [showSignupPassword, setShowSignupPassword] = useState(false);
    const [showForgotNewPassword, setShowForgotNewPassword] = useState(false);
    const [showForgotConfirmPassword, setShowForgotConfirmPassword] = useState(false);

    // Form inputs
    const [loginForm, setLoginForm] = useState({ username: '', password: '' });
    const [signupForm, setSignupForm] = useState({ username: '', email: '', password: '' });

    // Forgot Password state
    const [forgotStep, setForgotStep] = useState(1); // 1: Request OTP, 2: Verify OTP, 3: Reset Password
    const [forgotIdentifier, setForgotIdentifier] = useState('');
    const [forgotOtp, setForgotOtp] = useState('');
    const [forgotNewPassword, setForgotNewPassword] = useState('');
    const [forgotConfirmPassword, setForgotConfirmPassword] = useState('');
    const [resendTimer, setResendTimer] = useState(0);
    const [otpNoticeInfo, setOtpNoticeInfo] = useState({ emailSent: false, devOtp: '', message: '' });

    useEffect(() => {
        let interval = null;
        if (resendTimer > 0) {
            interval = setInterval(() => {
                setResendTimer((prev) => prev - 1);
            }, 1000);
        }
        return () => {
            if (interval) clearInterval(interval);
        };
    }, [resendTimer]);

    useEffect(() => {
        if (searchParams.get('error') === 'admin_required') {
            showToast('Admin privileges required. Sign in as Administrator.', 'error');
        } else if (searchParams.get('error') === 'login_required') {
            showToast('Please sign in to access your workspace.', 'error');
        } else if (searchParams.get('session_expired') === 'true') {
            showToast('Session expired. Please sign in again.', 'error');
        }

        const registered = JSON.parse(localStorage.getItem('simulated_registered_users') || '[]');
        if (registered.length === 0) {
            registered.push({
                username: 'user',
                email: 'user@example.com',
                password: 'password123'
            });
            localStorage.setItem('simulated_registered_users', JSON.stringify(registered));
        }
    }, [searchParams, showToast]);

    const fillAdminCreds = () => {
        setLoginForm({ username: 'admin', password: 'admin123' });
        setTab('login');
        showToast('Admin credentials filled', 'info');
    };

    const fillUserCreds = () => {
        setLoginForm({ username: 'user', password: 'password123' });
        setTab('login');
        showToast('Demo user credentials filled', 'info');
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        const username = loginForm.username.trim();
        const password = loginForm.password;

        if (!username || !password) {
            showToast('Please enter both username and password', 'error');
            return;
        }

        setLoading(true);

        try {
            if (username === 'admin') {
                const res = await API.loginAdmin(username, password);
                if (res.status === 'success' && res.access_token) {
                    loginAdmin(res.access_token, username);
                    showToast('Signed in as Administrator!', 'success');
                    const redirectUrl = searchParams.get('redirect') || '/admin';
                    setTimeout(() => navigate(redirectUrl), 600);
                } else {
                    throw new Error(res.message || 'Invalid admin credentials');
                }
            } else {
                try {
                    const res = await API.loginUser(username, password);
                    if (res.status === 'success') {
                        loginUser(res.username || username, res.email || `${username}@example.com`);
                        showToast(`Welcome back, ${res.username || username}!`, 'success');
                        const redirectUrl = searchParams.get('redirect') || '/';
                        setTimeout(() => navigate(redirectUrl), 600);
                        return;
                    }
                } catch (apiErr) {
                    // Fallback to local storage check if API is unreachable
                    const registered = JSON.parse(localStorage.getItem('simulated_registered_users') || '[]');
                    const matchedUser = registered.find(
                        (u) => u.username.toLowerCase() === username.toLowerCase() || u.email.toLowerCase() === username.toLowerCase()
                    );

                    if (!matchedUser) {
                        throw new Error(apiErr.message || 'Account not found. Click "Register" to create an account.');
                    }

                    if (matchedUser.password !== password) {
                        throw new Error('Incorrect password. Click "Forgot password?" to reset.');
                    }

                    loginUser(matchedUser.username, matchedUser.email);
                    showToast(`Welcome back, ${matchedUser.username}!`, 'success');
                    const redirectUrl = searchParams.get('redirect') || '/';
                    setTimeout(() => navigate(redirectUrl), 600);
                }
            }
        } catch (err) {
            showToast(err.message || 'Sign in failed. Verify credentials.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        if (!signupForm.username || !signupForm.email || !signupForm.password) {
            showToast('Please fill out all fields', 'error');
            return;
        }
        if (signupForm.password.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            return;
        }

        setLoading(true);

        const uName = signupForm.username.trim();
        const uEmail = signupForm.email.trim();
        const uPass = signupForm.password;

        try {
            const res = await API.registerUser(uName, uEmail, uPass);
            if (res.status === 'success') {
                loginUser(uName, uEmail);
                showToast(`Account registered! Welcome, ${uName}!`, 'success');
                const redirectUrl = searchParams.get('redirect') || '/';
                setTimeout(() => navigate(redirectUrl), 600);
                return;
            }
        } catch (err) {
            const registered = JSON.parse(localStorage.getItem('simulated_registered_users') || '[]');
            if (registered.some((u) => u.username.toLowerCase() === uName.toLowerCase())) {
                showToast('Username already exists. Choose a different one.', 'error');
                setLoading(false);
                return;
            }
            registered.push({
                username: uName,
                email: uEmail,
                password: uPass
            });
            localStorage.setItem('simulated_registered_users', JSON.stringify(registered));
            loginUser(uName, uEmail);
            showToast(`Account registered! Welcome, ${uName}!`, 'success');
            const redirectUrl = searchParams.get('redirect') || '/';
            setTimeout(() => navigate(redirectUrl), 600);
            return;
        } finally {
            setLoading(false);
        }
    };

    // ---------------- FORGOT PASSWORD OTP WORKFLOW ----------------

    // STEP 1: Request OTP
    const handleForgotRequestOtp = async (e) => {
        e.preventDefault();
        const identifier = forgotIdentifier.trim().toLowerCase();
        if (!identifier) {
            showToast('Please enter your email or username', 'error');
            return;
        }

        setLoading(true);

        try {
            const res = await API.requestForgotPasswordOtp(identifier);
            const devCode = res.dev_otp || '';
            setOtpNoticeInfo({
                emailSent: !!res.email_sent,
                devOtp: devCode,
                message: res.message || ''
            });
            setForgotOtp('');
            setForgotStep(2);
            setResendTimer(60);
            if (res.email_sent) {
                showToast(res.message || 'A 6-digit OTP verification code has been sent directly to your email inbox!', 'success');
            } else {
                showToast('Unable to send OTP email to inbox. Please check your SMTP settings in .env file.', 'error');
            }
        } catch (err) {
            setOtpNoticeInfo({
                emailSent: false,
                devOtp: '',
                message: err.message || 'Failed to send OTP code.'
            });
            setForgotOtp('');
            setForgotStep(2);
            setResendTimer(60);
            showToast('Unable to dispatch OTP email. Check network & SMTP settings in .env.', 'error');
        } finally {
            setLoading(false);
        }
    };

    // Resend OTP Code
    const handleResendOtp = async () => {
        if (resendTimer > 0) return;
        const identifier = forgotIdentifier.trim().toLowerCase();
        if (!identifier) {
            showToast('Identifier is required to resend OTP', 'error');
            return;
        }

        setLoading(true);

        try {
            const res = await API.requestForgotPasswordOtp(identifier);
            const devCode = res.dev_otp || '';
            setOtpNoticeInfo({
                emailSent: !!res.email_sent,
                devOtp: devCode,
                message: res.message || ''
            });
            setForgotOtp('');
            setResendTimer(60);
            if (res.email_sent) {
                showToast(res.message || 'A new 6-digit OTP code has been sent to your email inbox!', 'success');
            } else {
                showToast('Unable to resend email. Check your SMTP settings in .env file.', 'error');
            }
        } catch (err) {
            setOtpNoticeInfo({
                emailSent: false,
                devOtp: '',
                message: err.message || 'Failed to resend OTP.'
            });
            setForgotOtp('');
            setResendTimer(60);
            showToast('Unable to resend OTP email. Check network & SMTP settings in .env.', 'error');
        } finally {
            setLoading(false);
        }
    };

    // STEP 2: Verify OTP
    const handleForgotVerifyOtp = async (e) => {
        e.preventDefault();
        const identifier = forgotIdentifier.trim().toLowerCase();
        const otp = forgotOtp.trim();

        if (!otp) {
            showToast('Please enter the 6-digit OTP code sent to your email', 'error');
            return;
        }

        setLoading(true);

        try {
            const res = await API.verifyForgotPasswordOtp(identifier, otp);
            if (res.status === 'success') {
                setForgotStep(3);
                showToast('OTP verified successfully! Set your new password.', 'success');
            } else {
                throw new Error(res.message || 'Invalid OTP code');
            }
        } catch (err) {
            showToast(err.message || 'Invalid or expired OTP code. Please enter the exact code sent to your email.', 'error');
        } finally {
            setLoading(false);
        }
    };

    // STEP 3: Reset Password
    const handleForgotResetPassword = async (e) => {
        e.preventDefault();
        const identifier = forgotIdentifier.trim().toLowerCase();
        const otp = forgotOtp.trim();

        if (!forgotNewPassword || !forgotConfirmPassword) {
            showToast('Please enter and confirm your new password', 'error');
            return;
        }
        if (forgotNewPassword.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            return;
        }
        if (forgotNewPassword !== forgotConfirmPassword) {
            showToast('Passwords do not match. Re-enter.', 'error');
            return;
        }

        setLoading(true);

        try {
            const res = await API.resetPasswordWithOtp(identifier, otp, forgotNewPassword);
            if (res.status === 'success') {
                showToast(res.message || 'Password reset successfully!', 'success');
                setLoginForm({ username: identifier, password: forgotNewPassword });
                setForgotStep(1);
                setForgotIdentifier('');
                setForgotOtp('');
                setForgotNewPassword('');
                setForgotConfirmPassword('');
                setTab('login');
            } else {
                throw new Error(res.message || 'Failed to reset password');
            }
        } catch (err) {
            showToast(err.message || 'Failed to reset password. Please check your credentials and try again.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const getStrengthScore = (pwd) => {
        if (!pwd) return 0;
        let score = 0;
        if (pwd.length >= 6) score++;
        if (/[A-Z]/.test(pwd) || /[0-9]/.test(pwd)) score++;
        if (/[^A-Za-z0-9]/.test(pwd) && pwd.length >= 8) score++;
        return score;
    };

    const getStrengthLabel = (pwd) => {
        const score = getStrengthScore(pwd);
        if (score <= 1) return 'Weak password';
        if (score === 2) return 'Good password';
        return 'Strong password';
    };

    return (
        <div className="min-h-screen bg-dark-900 flex items-center justify-center p-4 md:p-8">
            <div className="w-full max-w-4xl card-studio grid grid-cols-1 md:grid-cols-2 overflow-hidden shadow-2xl">
                {/* LEFT PANE: Branding Showcase */}
                <div className="hidden md:flex flex-col justify-between p-8 bg-gradient-to-br from-slate-900 via-dark-900 to-cyan-950/40 border-r border-white/5 relative">
                    <div className="space-y-6">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-white shadow-lg">
                                <Brain className="w-5 h-5" />
                            </div>
                            <span className="text-xl font-bold text-white tracking-tight">AlgoGen Studio</span>
                        </div>

                        <div className="space-y-2">
                            <h2 className="text-2xl font-extrabold text-white leading-tight">
                                Intelligent Algorithm Generation & Synthesis Engine
                            </h2>
                            <p className="text-xs text-slate-400 leading-relaxed">
                                Join developers and researchers using Hybrid GA-RL optimization to synthesize algorithms on demand.
                            </p>
                        </div>
                    </div>

                    <div className="pt-6 border-t border-white/5 text-[11px] text-slate-500 font-mono">
                        FastAPI Backend Target: http://localhost:8000
                    </div>
                </div>

                {/* RIGHT PANE: Auth Forms */}
                <div className="p-8 flex flex-col justify-between">
                    <div>
                        {/* Header Tabs */}
                        {tab !== 'forgot' && (
                            <div className="flex border-b border-white/10 mb-6">
                                <button
                                    onClick={() => setTab('login')}
                                    className={`flex-1 py-3 text-center border-b-2 text-xs font-bold transition ${tab === 'login' ? 'border-cyan-400 text-white' : 'border-transparent text-slate-400 hover:text-white'
                                        }`}
                                >
                                    Sign In
                                </button>
                                <button
                                    onClick={() => setTab('signup')}
                                    className={`flex-1 py-3 text-center border-b-2 text-xs font-bold transition ${tab === 'signup' ? 'border-cyan-400 text-white' : 'border-transparent text-slate-400 hover:text-white'
                                        }`}
                                >
                                    Register
                                </button>
                            </div>
                        )}

                        {/* Tab: SIGN IN */}
                        {tab === 'login' && (
                            <div className="space-y-4">
                                <div>
                                    <h2 className="text-xl font-bold text-white tracking-tight">Welcome back</h2>
                                    <p className="text-xs text-slate-400 mt-1">Sign in to access your workspace and search history.</p>
                                </div>

                                <form onSubmit={handleLogin} className="space-y-3.5">
                                    <div className="space-y-1">
                                        <label className="text-xs text-slate-300 font-semibold">Username / Admin ID</label>
                                        <div className="relative">
                                            <User className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                            <input
                                                type="text"
                                                value={loginForm.username}
                                                onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                                                required
                                                placeholder="e.g. admin or user"
                                                className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100 placeholder-slate-500"
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-1">
                                        <div className="flex justify-between items-center">
                                            <label className="text-xs text-slate-300 font-semibold">Password</label>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    setForgotStep(1);
                                                    setForgotOtp('');
                                                    setTab('forgot');
                                                }}
                                                className="text-[11px] text-cyan-400 hover:underline font-medium"
                                            >
                                                Forgot password?
                                            </button>
                                        </div>
                                        <div className="relative">
                                            <Lock className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                            <input
                                                type={showLoginPassword ? 'text' : 'password'}
                                                value={loginForm.password}
                                                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                                                required
                                                placeholder="••••••••"
                                                className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-10 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100 placeholder-slate-500"
                                            />
                                            <button
                                                type="button"
                                                onClick={() => setShowLoginPassword(!showLoginPassword)}
                                                className="absolute right-3.5 top-3.5 text-slate-500 hover:text-slate-300 focus:outline-none"
                                            >
                                                {showLoginPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                            </button>
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        disabled={loading}
                                        className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2 mt-5 shadow-md shadow-cyan-600/20"
                                    >
                                        {loading ? (
                                            <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                        ) : (
                                            <>
                                                <span>Sign In</span>
                                                <ArrowRight className="w-3.5 h-3.5" />
                                            </>
                                        )}
                                    </button>
                                </form>

                                {/* Dev Quick-Fill Accounts */}
                                <div className="mt-4 p-3 rounded-xl bg-dark-900 border border-white/5 text-xs space-y-1.5">
                                    <span className="block text-slate-400 font-bold uppercase tracking-wider text-[10px]">Test Accounts:</span>
                                    <div className="grid grid-cols-2 gap-2">
                                        <button
                                            type="button"
                                            onClick={fillAdminCreds}
                                            className="py-1.5 px-2.5 rounded-lg bg-indigo-950/40 border border-indigo-500/20 hover:border-indigo-500/50 text-indigo-300 text-left transition flex flex-col"
                                        >
                                            <span className="font-bold flex items-center gap-1 text-[11px]">
                                                <Shield className="w-3 h-3 text-indigo-400" /> Admin
                                            </span>
                                            <span className="text-[10px] text-slate-400 font-mono">admin / admin123</span>
                                        </button>
                                        <button
                                            type="button"
                                            onClick={fillUserCreds}
                                            className="py-1.5 px-2.5 rounded-lg bg-white/5 border border-white/10 hover:border-white/20 text-slate-200 text-left transition flex flex-col"
                                        >
                                            <span className="font-bold flex items-center gap-1 text-[11px]">
                                                <User className="w-3 h-3 text-slate-400" /> Demo User
                                            </span>
                                            <span className="text-[10px] text-slate-400 font-mono">user / password123</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Tab: REGISTER */}
                        {tab === 'signup' && (
                            <div className="space-y-4">
                                <div>
                                    <h2 className="text-xl font-bold text-white tracking-tight">Create your account</h2>
                                    <p className="text-xs text-slate-400 mt-1">Register to start bookmarking algorithms.</p>
                                </div>

                                <form onSubmit={handleSignup} className="space-y-3.5">
                                    <div className="space-y-1">
                                        <label className="text-xs text-slate-300 font-semibold">Username</label>
                                        <div className="relative">
                                            <User className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                            <input
                                                type="text"
                                                value={signupForm.username}
                                                onChange={(e) => setSignupForm({ ...signupForm, username: e.target.value })}
                                                required
                                                placeholder="Choose a username"
                                                className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100"
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-1">
                                        <label className="text-xs text-slate-300 font-semibold">Email Address</label>
                                        <div className="relative">
                                            <Mail className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                            <input
                                                type="email"
                                                value={signupForm.email}
                                                onChange={(e) => setSignupForm({ ...signupForm, email: e.target.value })}
                                                required
                                                placeholder="you@example.com"
                                                className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100"
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-1">
                                        <label className="text-xs text-slate-300 font-semibold">Password</label>
                                        <div className="relative">
                                            <Lock className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                            <input
                                                type={showSignupPassword ? 'text' : 'password'}
                                                value={signupForm.password}
                                                onChange={(e) => setSignupForm({ ...signupForm, password: e.target.value })}
                                                required
                                                placeholder="At least 6 characters"
                                                className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-10 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100"
                                            />
                                            <button
                                                type="button"
                                                onClick={() => setShowSignupPassword(!showSignupPassword)}
                                                className="absolute right-3.5 top-3.5 text-slate-500 hover:text-slate-300 focus:outline-none"
                                            >
                                                {showSignupPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                            </button>
                                        </div>
                                        {signupForm.password.length > 0 && (
                                            <div className="space-y-1 pt-1">
                                                <div className="h-1.5 w-full bg-dark-900 rounded-full overflow-hidden flex">
                                                    <div
                                                        className={`h-full transition-all duration-300 ${getStrengthScore(signupForm.password) <= 1
                                                                ? 'w-1/3 bg-rose-500'
                                                                : getStrengthScore(signupForm.password) === 2
                                                                    ? 'w-2/3 bg-amber-500'
                                                                    : 'w-full bg-emerald-500'
                                                            }`}
                                                    ></div>
                                                </div>
                                                <span className="text-[10px] text-slate-400 block font-mono">
                                                    {getStrengthLabel(signupForm.password)}
                                                </span>
                                            </div>
                                        )}
                                    </div>

                                    <button
                                        type="submit"
                                        disabled={loading}
                                        className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2 mt-5 shadow-md shadow-cyan-600/20"
                                    >
                                        {loading ? (
                                            <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                        ) : (
                                            <span>Create Account</span>
                                        )}
                                    </button>
                                </form>
                            </div>
                        )}

                        {/* Tab: FORGOT PASSWORD (OTP AUTHENTICATION WORKFLOW) */}
                        {tab === 'forgot' && (
                            <div className="space-y-4">
                                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                                    <div className="flex items-center gap-2">
                                        <div className="w-6 h-6 rounded-md bg-cyan-600/20 border border-cyan-500/30 text-cyan-400 flex items-center justify-center font-bold text-xs">
                                            {forgotStep}/3
                                        </div>
                                        <div>
                                            <h2 className="text-sm font-bold text-white">Reset Password via OTP</h2>
                                            <p className="text-[10px] text-slate-400">
                                                {forgotStep === 1 && 'Step 1: Request 6-digit OTP'}
                                                {forgotStep === 2 && 'Step 2: Enter & Verify OTP'}
                                                {forgotStep === 3 && 'Step 3: Set New Password'}
                                            </p>
                                        </div>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => {
                                            setTab('login');
                                            setForgotStep(1);
                                        }}
                                        className="text-xs text-slate-400 hover:text-white transition"
                                    >
                                        <X className="w-4 h-4" />
                                    </button>
                                </div>

                                {/* STEP 1: Request OTP */}
                                {forgotStep === 1 && (
                                    <form onSubmit={handleForgotRequestOtp} className="space-y-3.5">
                                        <p className="text-xs text-slate-300 leading-relaxed">
                                            Enter the email address or username registered to your account to receive a 6-digit OTP authentication code.
                                        </p>

                                        <div className="space-y-1">
                                            <label className="text-xs text-slate-300 font-semibold">Email or Username</label>
                                            <div className="relative">
                                                <User className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                                <input
                                                    type="text"
                                                    value={forgotIdentifier}
                                                    onChange={(e) => setForgotIdentifier(e.target.value)}
                                                    required
                                                    placeholder="e.g. user@example.com or user"
                                                    className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100 placeholder-slate-500"
                                                />
                                            </div>
                                        </div>

                                        <div className="flex gap-2 pt-2">
                                            <button
                                                type="button"
                                                onClick={() => setTab('login')}
                                                className="flex-1 py-2.5 border border-white/10 hover:bg-white/5 text-slate-300 text-xs font-semibold rounded-xl transition text-center"
                                            >
                                                Cancel
                                            </button>
                                            <button
                                                type="submit"
                                                disabled={loading}
                                                className="flex-1 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-cyan-600/20"
                                            >
                                                {loading ? (
                                                    <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                                ) : (
                                                    <>
                                                        <KeyRound className="w-3.5 h-3.5" />
                                                        <span>Send OTP Code</span>
                                                    </>
                                                )}
                                            </button>
                                        </div>
                                    </form>
                                )}

                                {/* STEP 2: Verify OTP */}
                                {forgotStep === 2 && (
                                    <form onSubmit={handleForgotVerifyOtp} className="space-y-3.5">
                                        {/* Secure Email Delivery Notice */}
                                        {otpNoticeInfo.emailSent ? (
                                            <div className="p-3.5 rounded-xl bg-emerald-950/60 border border-emerald-500/40 text-xs text-emerald-200 space-y-1.5">
                                                <div className="flex items-center justify-between">
                                                    <span className="font-bold flex items-center gap-1.5 text-emerald-300">
                                                        <Mail className="w-4 h-4 text-emerald-400" />
                                                        Check Your Email Inbox
                                                    </span>
                                                    <span className="text-[10px] font-mono bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-400/30">
                                                        Valid for 10m
                                                    </span>
                                                </div>
                                                <p className="text-[11px] text-slate-300 leading-relaxed pt-0.5">
                                                    A 6-digit OTP verification code has been delivered to your email inbox. Open your email, copy the 6-digit code, and enter it below.
                                                </p>
                                            </div>
                                        ) : (
                                            <div className="p-3.5 rounded-xl bg-amber-950/60 border border-amber-500/40 text-xs text-amber-200 space-y-1.5">
                                                <div className="flex items-center justify-between">
                                                    <span className="font-bold flex items-center gap-1.5 text-amber-300">
                                                        <AlertTriangle className="w-4 h-4 text-amber-400" />
                                                        SMTP Credentials Required
                                                    </span>
                                                </div>
                                                <p className="text-[11px] text-amber-200/90 leading-relaxed pt-0.5">
                                                    Real email delivery is enabled, but SMTP authentication failed or placeholder credentials exist in .env. Update your SMTP_USER and SMTP_PASSWORD in .env to deliver emails to your inbox.
                                                </p>
                                            </div>
                                        )}

                                        <div className="space-y-1">
                                            <div className="flex items-center justify-between">
                                                <label className="text-xs text-slate-300 font-semibold">Enter 6-Digit OTP</label>
                                                <button
                                                    type="button"
                                                    onClick={handleResendOtp}
                                                    disabled={resendTimer > 0 || loading}
                                                    className={`text-[11px] font-medium transition flex items-center gap-1 ${
                                                        resendTimer > 0 
                                                            ? 'text-slate-500 cursor-not-allowed' 
                                                            : 'text-cyan-400 hover:text-cyan-300 hover:underline'
                                                    }`}
                                                >
                                                    <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
                                                    {resendTimer > 0 ? `Resend OTP (${resendTimer}s)` : 'Resend OTP'}
                                                </button>
                                            </div>
                                            <div className="relative">
                                                <KeyRound className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                                <input
                                                    type="text"
                                                    value={forgotOtp}
                                                    onChange={(e) => setForgotOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                                                    required
                                                    maxLength={6}
                                                    placeholder="6-digit numerical OTP"
                                                    className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-4 text-xs font-mono tracking-widest focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100 placeholder-slate-500"
                                                />
                                            </div>
                                            <p className="text-[11px] text-slate-400">
                                                Code sent for <strong className="text-slate-200">{forgotIdentifier}</strong>
                                            </p>
                                        </div>

                                        <div className="flex gap-2 pt-2">
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    setForgotStep(1);
                                                    setForgotOtp('');
                                                }}
                                                className="py-2.5 px-3 border border-white/10 hover:bg-white/5 text-slate-300 text-xs font-semibold rounded-xl transition text-center"
                                            >
                                                Back
                                            </button>
                                            <button
                                                type="submit"
                                                disabled={loading}
                                                className="flex-1 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-cyan-600/20"
                                            >
                                                {loading ? (
                                                    <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                                ) : (
                                                    <>
                                                        <span>Verify OTP</span>
                                                        <ArrowRight className="w-3.5 h-3.5" />
                                                    </>
                                                )}
                                            </button>
                                        </div>
                                    </form>
                                )}

                                {/* STEP 3: Reset Password */}
                                {forgotStep === 3 && (
                                    <form onSubmit={handleForgotResetPassword} className="space-y-3.5">
                                        <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 flex items-center gap-2.5 text-xs text-emerald-200">
                                            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                                            <div>
                                                <span className="font-bold block text-xs">OTP Verified Successfully</span>
                                                <span className="text-[10px] text-slate-400">
                                                    Updating password for {forgotIdentifier}
                                                </span>
                                            </div>
                                        </div>

                                        <div className="space-y-1">
                                            <label className="text-xs text-slate-300 font-semibold">New Password</label>
                                            <div className="relative">
                                                <Lock className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                                <input
                                                    type={showForgotNewPassword ? 'text' : 'password'}
                                                    value={forgotNewPassword}
                                                    onChange={(e) => setForgotNewPassword(e.target.value)}
                                                    required
                                                    placeholder="Minimum 6 characters"
                                                    className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-10 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100"
                                                />
                                                <button
                                                    type="button"
                                                    onClick={() => setShowForgotNewPassword(!showForgotNewPassword)}
                                                    className="absolute right-3.5 top-3.5 text-slate-500 hover:text-slate-300 focus:outline-none"
                                                >
                                                    {showForgotNewPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                                </button>
                                            </div>
                                        </div>

                                        <div className="space-y-1">
                                            <label className="text-xs text-slate-300 font-semibold">Confirm New Password</label>
                                            <div className="relative">
                                                <Lock className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3.5" />
                                                <input
                                                    type={showForgotConfirmPassword ? 'text' : 'password'}
                                                    value={forgotConfirmPassword}
                                                    onChange={(e) => setForgotConfirmPassword(e.target.value)}
                                                    required
                                                    placeholder="Re-enter new password"
                                                    className="w-full bg-dark-900 border border-white/10 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-10 text-xs focus:outline-none focus:ring-1 focus:ring-cyan-500 transition text-slate-100"
                                                />
                                                <button
                                                    type="button"
                                                    onClick={() => setShowForgotConfirmPassword(!showForgotConfirmPassword)}
                                                    className="absolute right-3.5 top-3.5 text-slate-500 hover:text-slate-300 focus:outline-none"
                                                >
                                                    {showForgotConfirmPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                                </button>
                                            </div>
                                        </div>

                                        <div className="flex gap-2 pt-2">
                                            <button
                                                type="button"
                                                onClick={() => setForgotStep(2)}
                                                className="py-2.5 px-3 border border-white/10 hover:bg-white/5 text-slate-300 text-xs font-semibold rounded-xl transition text-center"
                                            >
                                                Back
                                            </button>
                                            <button
                                                type="submit"
                                                disabled={loading}
                                                className="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-emerald-600/20"
                                            >
                                                {loading ? (
                                                    <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                                ) : (
                                                    <>
                                                        <CheckCircle2 className="w-3.5 h-3.5" />
                                                        <span>Reset Password</span>
                                                    </>
                                                )}
                                            </button>
                                        </div>
                                    </form>
                                )}
                            </div>
                        )}
                    </div>

                    <div className="pt-4 border-t border-white/5 text-center">
                        <button
                            onClick={() => navigate('/')}
                            className="text-xs text-slate-400 hover:text-white transition flex items-center justify-center gap-1.5 mx-auto"
                        >
                            <ArrowLeft className="w-3.5 h-3.5" /> Return to Studio Homepage
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

