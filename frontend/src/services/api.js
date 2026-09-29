/**
 * API Integration Layer for FastAPI Backend (http://localhost:8000)
 */

const API_BASE_URL = 'http://localhost:8000';

async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };
    
    const token = localStorage.getItem('admin_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    try {
        const response = await fetch(url, config);
        
        if (response.status === 401) {
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login?session_expired=true';
            }
            throw new Error('Unauthorized session. Please sign in again.');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || `API Error: ${response.statusText}`);
        }
        
        return data;
    } catch (error) {
        console.error(`API Fetch Error on ${endpoint}:`, error);
        throw error;
    }
}

export const API = {
    loginAdmin: async (username, password) => {
        return apiFetch('/admin/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    getHealth: async () => {
        return apiFetch('/health');
    },

    getAllAlgorithms: async () => {
        return apiFetch('/algorithms');
    },

    getAlgorithmLeetCode: async (name) => {
        return apiFetch(`/algorithm/${encodeURIComponent(name)}/leetcode`);
    },

    getAlgorithmByName: async (name) => {
        return apiFetch(`/algorithm/${encodeURIComponent(name)}`);
    },

    askInterviewQuestion: async (name, question) => {
        return apiFetch(`/algorithm/${encodeURIComponent(name)}/ask-interview`, {
            method: 'POST',
            body: JSON.stringify({ question })
        });
    },

    getAlgorithmsByCategory: async (category) => {
        return apiFetch(`/category/${encodeURIComponent(category)}`);
    },

    getAlgorithmsByKeyword: async (keyword) => {
        return apiFetch(`/keyword/${encodeURIComponent(keyword)}`);
    },

    getAlgorithmsByApplication: async (application) => {
        return apiFetch(`/application/${encodeURIComponent(application)}`);
    },

    solveProblem: async (problemText) => {
        return apiFetch('/problem/solve', {
            method: 'POST',
            body: JSON.stringify({ problem: problemText })
        });
    },

    trainProblem: async (params) => {
        return apiFetch('/problem/train', {
            method: 'POST',
            body: JSON.stringify(params || {})
        });
    },

    evaluateProblem: async (params) => {
        return apiFetch('/problem/evaluate', {
            method: 'POST',
            body: JSON.stringify(params || {})
        });
    },

    runProblemCode: async (code) => {
        return apiFetch('/problem/run-code', {
            method: 'POST',
            body: JSON.stringify({ code })
        });
    },


    getBackendStatistics: async () => {
        return apiFetch('/statistics');
    },

    getDashboardAnalytics: async () => {
        return apiFetch('/dashboard');
    },

    getPerformanceMetrics: async () => {
        return apiFetch('/performance');
    },

    getTopPerformance: async () => {
        return apiFetch('/performance/top');
    },

    getRecentSearches: async () => {
        return apiFetch('/query/recent');
    },

    getGenerationLogs: async () => {
        return apiFetch('/logs/generation');
    },

    getApiLogs: async () => {
        return apiFetch('/logs/api');
    },

    // Admin CRUD operations
    createAlgorithm: async (algorithmData) => {
        return apiFetch('/admin/algorithm', {
            method: 'POST',
            body: JSON.stringify(algorithmData)
        });
    },

    updateAlgorithm: async (name, algorithmData) => {
        return apiFetch(`/admin/algorithm/${encodeURIComponent(name)}`, {
            method: 'PUT',
            body: JSON.stringify(algorithmData)
        });
    },

    deleteAlgorithm: async (name) => {
        return apiFetch(`/admin/algorithm/${encodeURIComponent(name)}`, {
            method: 'DELETE'
        });
    },

    // Auth & OTP endpoints
    loginUser: async (username, password) => {
        return apiFetch('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    registerUser: async (username, email, password) => {
        return apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password })
        });
    },

    requestForgotPasswordOtp: async (identifier) => {
        return apiFetch('/auth/forgot-password/request-otp', {
            method: 'POST',
            body: JSON.stringify({ identifier })
        });
    },

    verifyForgotPasswordOtp: async (identifier, otp) => {
        return apiFetch('/auth/forgot-password/verify-otp', {
            method: 'POST',
            body: JSON.stringify({ identifier, otp })
        });
    },

    resetPasswordWithOtp: async (identifier, otp, newPassword) => {
        return apiFetch('/auth/forgot-password/reset-password', {
            method: 'POST',
            body: JSON.stringify({ identifier, otp, new_password: newPassword })
        });
    }
};
