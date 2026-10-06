import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useAuth } from './AuthContext';

const UserHistoryContext = createContext();

export function UserHistoryProvider({ children }) {
    const { currentUser } = useAuth();
    const [history, setHistory] = useState([]);
    const [bookmarks, setBookmarks] = useState([]);

    const getActiveUsername = useCallback(() => {
        if (currentUser && currentUser.username) {
            return currentUser.username.toLowerCase();
        }
        return 'guest';
    }, [currentUser]);

    const getHistoryKey = useCallback(() => {
        return `user_search_history_${getActiveUsername()}`;
    }, [getActiveUsername]);

    const getBookmarkKey = useCallback(() => {
        return `user_bookmarks_${getActiveUsername()}`;
    }, [getActiveUsername]);

    // Sync history & bookmarks whenever user changes
    useEffect(() => {
        const hKey = getHistoryKey();
        const bKey = getBookmarkKey();

        const storedHistory = JSON.parse(localStorage.getItem(hKey) || '[]');
        const storedBookmarks = JSON.parse(localStorage.getItem(bKey) || '[]');

        setHistory(storedHistory);
        setBookmarks(storedBookmarks);
    }, [getHistoryKey, getBookmarkKey]);

    const addHistory = useCallback((query, type, status) => {
        const key = getHistoryKey();
        const current = JSON.parse(localStorage.getItem(key) || '[]');
        const updated = [
            {
                query,
                type,
                status,
                timestamp: new Date().toISOString()
            },
            ...current
        ].slice(0, 50);

        localStorage.setItem(key, JSON.stringify(updated));
        setHistory(updated);
    }, [getHistoryKey]);

    const clearHistory = useCallback(() => {
        const key = getHistoryKey();
        localStorage.removeItem(key);
        setHistory([]);
    }, [getHistoryKey]);

    const toggleBookmark = useCallback((algorithmName) => {
        const key = getBookmarkKey();
        let current = JSON.parse(localStorage.getItem(key) || '[]');
        let isAdded = false;

        if (current.includes(algorithmName)) {
            current = current.filter((b) => b !== algorithmName);
            isAdded = false;
        } else {
            current.push(algorithmName);
            isAdded = true;
        }

        localStorage.setItem(key, JSON.stringify(current));
        setBookmarks(current);
        return isAdded;
    }, [getBookmarkKey]);

    const isBookmarked = useCallback((algorithmName) => {
        return bookmarks.includes(algorithmName);
    }, [bookmarks]);

    return (
        <UserHistoryContext.Provider
            value={{
                history,
                bookmarks,
                addHistory,
                clearHistory,
                toggleBookmark,
                isBookmarked
            }}
        >
            {children}
        </UserHistoryContext.Provider>
    );
}

export function useUserHistory() {
    return useContext(UserHistoryContext);
}
