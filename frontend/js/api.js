/**
 * API Integration Layer for Algorithm Generator Backend
 * Maps to backend running at http://localhost:8000
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Shared fetch wrapper that handles credentials, headers, and error parsing
 */
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Inject headers
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };
    
    // Inject auth token if available in localStorage
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
        
        // Handle 401 unauthorized (expired or invalid token)
        if (response.status === 401) {
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            // Avoid infinite redirects if already on login page
            if (!window.location.pathname.includes('login.html')) {
                const isSubpage = window.location.pathname.includes('/pages/');
                const loginRedirect = isSubpage ? 'login.html' : 'pages/login.html';
                window.location.href = loginRedirect + '?session_expired=true';
            }
            throw new Error('Unauthorized session. Please login again.');
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

const API = {
    // ==========================================
    // AUTH ENPOINTS
    // ==========================================

    /**
     * POST /admin/login
     * Logs in the admin with static credentials (admin / admin123)
     */
    loginAdmin: async (username, password) => {
        return apiFetch('/admin/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    // ==========================================
    // SYSTEM HEALTH
    // ==========================================

    /**
     * GET /health
     * Check backend and MongoDB connection status
     */
    getHealth: async () => {
        return apiFetch('/health');
    },

    // ==========================================
    // ALGORITHMS (PUBLIC & USER PORTAL)
    // ==========================================

    /**
     * GET /algorithms
     * Retrieves all algorithms from database
     */
    getAllAlgorithms: async () => {
        return apiFetch('/algorithms');
    },

    /**
     * GET /algorithm/{algorithm_name}
     * Retrieves a single algorithm by name. If not found in DB,
     * triggers OpenRouter AI generation and saves to DB automatically.
     */
    getAlgorithmByName: async (name) => {
        return apiFetch(`/algorithm/${encodeURIComponent(name)}`);
    },

    /**
     * GET /category/{category_name}
     * Search algorithms by category matching (regex)
     */
    getAlgorithmsByCategory: async (category) => {
        return apiFetch(`/category/${encodeURIComponent(category)}`);
    },

    /**
     * GET /keyword/{keyword}
     * Search algorithms by keyword matching (regex)
     */
    getAlgorithmsByKeyword: async (keyword) => {
        return apiFetch(`/keyword/${encodeURIComponent(keyword)}`);
    },

    /**
     * GET /application/{application}
     * Search algorithms by application matching (regex)
     */
    getAlgorithmsByApplication: async (application) => {
        return apiFetch(`/application/${encodeURIComponent(application)}`);
    },

    /**
     * GET /statistics
     * Retrieves backend statistics (query status counts, retrieval counts, etc.)
     */
    getBackendStatistics: async () => {
        return apiFetch('/statistics');
    },

    /**
     * GET /performance
     * Retrieves all performance records
     */
    getPerformanceMetrics: async () => {
        return apiFetch('/performance');
    },

    /**
     * GET /performance/top
     * Retrieves top 10 most searched algorithms
     */
    getTopPerformance: async () => {
        return apiFetch('/performance/top');
    },

    // ==========================================
    // ADMIN ALGORITHM CRUD (PROTECTED)
    // ==========================================

    /**
     * GET /admin/algorithms
     * Retrieves all algorithms (Admin dashboard detail list)
     */
    adminGetAlgorithms: async () => {
        return apiFetch('/admin/algorithms');
    },

    /**
     * POST /admin/algorithm
     * Add new manual algorithm to the repository
     */
    adminAddAlgorithm: async (algorithmData) => {
        return apiFetch('/admin/algorithm', {
            method: 'POST',
            body: JSON.stringify(algorithmData)
        });
    },

    /**
     * PUT /admin/algorithm/{algorithm_name}
     * Updates an algorithm's description
     */
    adminUpdateAlgorithm: async (name, description) => {
        return apiFetch(`/admin/algorithm/${encodeURIComponent(name)}`, {
            method: 'PUT',
            body: JSON.stringify({ description })
        });
    },

    /**
     * DELETE /admin/algorithm/{algorithm_name}
     * Deletes an algorithm from the database
     */
    adminDeleteAlgorithm: async (name) => {
        return apiFetch(`/admin/algorithm/${encodeURIComponent(name)}`, {
            method: 'DELETE'
        });
    },

    // ==========================================
    // DASHBOARD ANALYTICS (PUBLIC / ADMIN)
    // ==========================================

    /**
     * GET /dashboard
     * Retrieves main dashboard statistics
     */
    getDashboardAnalytics: async () => {
        return apiFetch('/dashboard');
    },

    /**
     * GET /dashboard/top-algorithms
     * Retrieves top 3 most searched algorithms for dashboards
     */
    getDashboardTopAlgorithms: async () => {
        return apiFetch('/dashboard/top-algorithms');
    },

    /**
     * GET /dashboard/recent-searches
     * Retrieves 10 most recent search queries
     */
    getRecentSearches: async () => {
        return apiFetch('/dashboard/recent-searches');
    },

    /**
     * GET /dashboard/api-usage
     * Retrieves aggregate log info grouped by API endpoints
     */
    getApiUsage: async () => {
        return apiFetch('/dashboard/api-usage');
    },

    /**
     * GET /dashboard/generation-analytics
     * Retrieves totals for AI generations: generated, retrieved, failed
     */
    getGenerationAnalytics: async () => {
        return apiFetch('/dashboard/generation-analytics');
    }
};

// Export to window object for access in multi-page environment
window.API = API;
window.API_BASE_URL = API_BASE_URL;
