/**
 * Global App Logic & Authentication Guards
 */

// Global Alpine.js initialization
document.addEventListener('alpine:init', () => {
    // ----------------------------------------
    // Toast Notification System
    // ----------------------------------------
    Alpine.store('toasts', {
        list: [],
        add(message, type = 'success', duration = 4000) {
            const id = Date.now() + Math.random().toString(36).substr(2, 9);
            this.list.push({ id, message, type });
            
            setTimeout(() => {
                this.remove(id);
            }, duration);
        },
        remove(id) {
            this.list = this.list.filter(toast => toast.id !== id);
        }
    });

    // ----------------------------------------
    // Global Auth State
    // ----------------------------------------
    Alpine.store('auth', {
        // State fields
        isAdmin: !!localStorage.getItem('admin_token'),
        isUser: !!localStorage.getItem('user_session'),
        currentUser: null,

        init() {
            if (this.isAdmin) {
                this.currentUser = JSON.parse(localStorage.getItem('admin_user') || '{"username": "admin"}');
            } else if (this.isUser) {
                this.currentUser = JSON.parse(localStorage.getItem('user_session'));
            }
        },

        loginAdmin(token, username) {
            localStorage.setItem('admin_token', token);
            localStorage.setItem('admin_user', JSON.stringify({ username, role: 'admin' }));
            localStorage.removeItem('user_session'); // Clear user session if logging in as admin
            this.isAdmin = true;
            this.isUser = false;
            this.currentUser = { username, role: 'admin' };
        },

        loginUser(username, email) {
            const user = { username, email, role: 'user', loginTime: new Date() };
            localStorage.setItem('user_session', JSON.stringify(user));
            localStorage.removeItem('admin_token'); // Clear admin session
            localStorage.removeItem('admin_user');
            this.isAdmin = false;
            this.isUser = true;
            this.currentUser = user;
        },

        logout() {
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            localStorage.removeItem('user_session');
            this.isAdmin = false;
            this.isUser = false;
            this.currentUser = null;
            
            // Redirect to home
            const isSubpage = window.location.pathname.includes('/pages/');
            window.location.href = isSubpage ? 'login.html' : 'pages/login.html';
        }
    });
});

/**
 * Toast Dispatcher (accessible outside Alpine environment)
 */
window.showToast = (message, type = 'success') => {
    // Wait until Alpine is loaded to show toasts
    if (window.Alpine) {
        window.Alpine.store('toasts').add(message, type);
    } else {
        document.addEventListener('alpine:init', () => {
            window.Alpine.store('toasts').add(message, type);
        });
    }
};

/**
 * Route protection guard
 * Redirects unauthorized users
 */
function runRouteGuard() {
    const path = window.location.pathname;
    const isAdmin = !!localStorage.getItem('admin_token');
    const isUser = !!localStorage.getItem('user_session');
    
    // Admin only pages
    const adminPages = [
        'admin-dashboard.html',
        'admin-algorithms.html'
    ];
    
    // User or Admin only pages
    const protectedPages = [
        'dashboard.html'
    ];

    const isCurrentAdminPage = adminPages.some(page => path.includes(page));
    const isCurrentProtectedPage = protectedPages.some(page => path.includes(page));

    const isSubpage = path.includes('/pages/');
    const loginRedirect = isSubpage ? 'login.html' : 'pages/login.html';

    if (isCurrentAdminPage && !isAdmin) {
        console.warn('Unauthorized admin access. Redirecting...');
        window.location.href = loginRedirect + '?redirect=' + encodeURIComponent(window.location.pathname) + '&error=admin_required';
    } else if (isCurrentProtectedPage && !isAdmin && !isUser) {
        console.warn('Authentication required. Redirecting...');
        window.location.href = loginRedirect + '?redirect=' + encodeURIComponent(window.location.pathname) + '&error=login_required';
    }
}

// Run routing guard immediately on load
runRouteGuard();

// Simulated database utilities for normal user history (stores locally)
const UserHistory = {
    getHistory() {
        return JSON.parse(localStorage.getItem('user_search_history') || '[]');
    },
    addHistory(query, type, status) {
        const history = this.getHistory();
        history.unshift({
            query,
            type,
            status,
            timestamp: new Date().toISOString()
        });
        // Limit to 50 items
        localStorage.setItem('user_search_history', JSON.stringify(history.slice(0, 50)));
    },
    clearHistory() {
        localStorage.removeItem('user_search_history');
    },
    getBookmarks() {
        return JSON.parse(localStorage.getItem('user_bookmarks') || '[]');
    },
    toggleBookmark(algorithmName) {
        let bookmarks = this.getBookmarks();
        if (bookmarks.includes(algorithmName)) {
            bookmarks = bookmarks.filter(b => b !== algorithmName);
            localStorage.setItem('user_bookmarks', JSON.stringify(bookmarks));
            return false; // removed
        } else {
            bookmarks.push(algorithmName);
            localStorage.setItem('user_bookmarks', JSON.stringify(bookmarks));
            return true; // added
        }
    }
};

window.UserHistory = UserHistory;
