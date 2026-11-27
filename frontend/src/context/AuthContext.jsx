import React, { createContext, useContext, useState, useEffect } from 'react';
import { API } from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [isAdmin, setIsAdmin] = useState(!!localStorage.getItem('admin_token'));
    const [isUser, setIsUser] = useState(!!localStorage.getItem('user_session'));
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        if (isAdmin) {
            const user = JSON.parse(localStorage.getItem('admin_user') || '{"username": "admin", "role": "admin"}');
            setCurrentUser(user);
        } else if (isUser) {
            const user = JSON.parse(localStorage.getItem('user_session') || 'null');
            setCurrentUser(user);
        } else {
            setCurrentUser(null);
        }
    }, [isAdmin, isUser]);

    const loginAdmin = (token, username) => {
        localStorage.setItem('admin_token', token);
        const adminUser = { username, role: 'admin' };
        localStorage.setItem('admin_user', JSON.stringify(adminUser));
        localStorage.removeItem('user_session');
        setIsAdmin(true);
        setIsUser(false);
        setCurrentUser(adminUser);
    };

    const loginUser = (username, email) => {
        const user = { username, email, role: 'user', loginTime: new Date() };
        localStorage.setItem('user_session', JSON.stringify(user));
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_user');
        setIsAdmin(false);
        setIsUser(true);
        setCurrentUser(user);
    };

    const logout = () => {
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_user');
        localStorage.removeItem('user_session');
        setIsAdmin(false);
        setIsUser(false);
        setCurrentUser(null);
        window.location.href = '/login';
    };

    return (
        <AuthContext.Provider value={{ isAdmin, isUser, currentUser, loginAdmin, loginUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
