"""
Svelte stores and composables generator for monorepo bootstrap.
Extracts stores and state management functionality from the main Svelte generator.
"""

from pathlib import Path


class SvelteStoresComposablesGenerator:
    """
    Generator for Svelte stores, composables, and state management utilities.
    Handles auth stores, API composables, user composables, theme stores, etc.
    """

    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name

    def create_svelte_stores(self) -> None:
        """Create all Svelte stores for state management."""
        # Create auth store using proper Svelte 5 runes pattern
        auth_store = '''import type { User, LoginCredentials, RegisterData, AuthTokens } from '$types/auth.js';
import { browser } from '$app/environment';

// Export a reactive state object (recommended Svelte 5 pattern)
export const authState = $state({
  user: null as User | null,
  isAuthenticated: false,
  isLoading: false,
  error: null as string | null
});

// Initialize auth state from localStorage
export function initAuth() {
  if (!browser) return;

  try {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('auth_user');
    
    if (token && user) {
      const parsedUser = JSON.parse(user);
      authState.user = parsedUser;
      authState.isAuthenticated = true;
      authState.isLoading = false;
      authState.error = null;
    }
  } catch (error) {
    console.error('Failed to initialize auth state:', error);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  }
}

// Login user
export async function login(credentials: LoginCredentials): Promise<boolean> {
  authState.isLoading = true;
  authState.error = null;

  try {
    // Simulate API call - replace with actual endpoint
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const { user, tokens }: { user: User; tokens: AuthTokens } = await response.json();

    // Store tokens and user info
    if (browser) {
      localStorage.setItem('auth_token', tokens.accessToken);
      localStorage.setItem('refresh_token', tokens.refreshToken);
      localStorage.setItem('auth_user', JSON.stringify(user));
    }

    authState.user = user;
    authState.isAuthenticated = true;
    authState.isLoading = false;
    authState.error = null;

    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Login failed';
    authState.isLoading = false;
    authState.error = message;
    return false;
  }
}

// Register user
export async function register(data: RegisterData): Promise<boolean> {
  authState.isLoading = true;
  authState.error = null;

  try {
    const response = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    const { user, tokens }: { user: User; tokens: AuthTokens } = await response.json();

    if (browser) {
      localStorage.setItem('auth_token', tokens.accessToken);
      localStorage.setItem('refresh_token', tokens.refreshToken);
      localStorage.setItem('auth_user', JSON.stringify(user));
    }

    authState.user = user;
    authState.isAuthenticated = true;
    authState.isLoading = false;
    authState.error = null;

    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Registration failed';
    authState.isLoading = false;
    authState.error = message;
    return false;
  }
}

// Logout user
export function logout() {
  if (browser) {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('auth_user');
  }

  authState.user = null;
  authState.isAuthenticated = false;
  authState.isLoading = false;
  authState.error = null;
}

// Clear error
export function clearError() {
  authState.error = null;
}

// Update user profile
export async function updateProfile(updates: Partial<User>): Promise<boolean> {
  if (!authState.user) return false;

  authState.isLoading = true;

  try {
    const response = await fetch(`/api/v1/users/${authState.user.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      body: JSON.stringify(updates)
    });

    if (!response.ok) {
      throw new Error('Profile update failed');
    }

    const updatedUser: User = await response.json();

    if (browser) {
      localStorage.setItem('auth_user', JSON.stringify(updatedUser));
    }

    authState.user = updatedUser;
    authState.isLoading = false;

    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Profile update failed';
    authState.isLoading = false;
    authState.error = message;
    return false;
  }
}
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "auth.svelte.ts").write_text(auth_store)

        # Create theme store
        theme_store = '''import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'light' | 'dark';

interface ThemeState {
  current: Theme;
  preference: Theme | 'system';
}

function createThemeStore() {
  const { subscribe, set, update } = writable<ThemeState>({
    current: 'light',
    preference: 'system'
  });

  // Get system theme preference
  const getSystemTheme = (): Theme => {
    if (browser && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  };

  // Apply theme to document
  const applyTheme = (theme: Theme) => {
    if (browser) {
      document.documentElement.setAttribute('data-theme', theme);
      document.documentElement.classList.toggle('dark', theme === 'dark');
    }
  };

  // Initialize theme
  const init = () => {
    if (!browser) return;

    try {
      const stored = localStorage.getItem('theme_preference') as Theme | 'system' | null;
      const preference = stored || 'system';
      const current = preference === 'system' ? getSystemTheme() : preference;

      set({ current, preference });
      applyTheme(current);

      // Listen for system theme changes
      if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = (e: MediaQueryListEvent) => {
          update(state => {
            if (state.preference === 'system') {
              const newTheme = e.matches ? 'dark' : 'light';
              applyTheme(newTheme);
              return { ...state, current: newTheme };
            }
            return state;
          });
        };

        mediaQuery.addEventListener('change', handleChange);
      }
    } catch (error) {
      console.error('Failed to initialize theme:', error);
    }
  };

  return {
    subscribe,
    
    // Initialize the theme store
    init,

    // Set theme preference
    setTheme: (preference: Theme | 'system') => {
      const current = preference === 'system' ? getSystemTheme() : preference;
      
      update(state => ({ ...state, preference, current }));
      applyTheme(current);

      if (browser) {
        try {
          localStorage.setItem('theme_preference', preference);
        } catch (error) {
          console.error('Failed to save theme preference:', error);
        }
      }
    },

    // Toggle between light and dark (ignores system)
    toggle: () => {
      update(state => {
        const newTheme: Theme = state.current === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
        
        if (browser) {
          try {
            localStorage.setItem('theme_preference', newTheme);
          } catch (error) {
            console.error('Failed to save theme preference:', error);
          }
        }
        
        return { preference: newTheme, current: newTheme };
      });
    }
  };
}

export const themeStore = createThemeStore();
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "theme.ts").write_text(theme_store)

        # Create notifications store
        notifications_store = '''import { writable } from 'svelte/store';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  action?: {
    label: string;
    handler: () => void;
  };
  timestamp: Date;
}

function createNotificationStore() {
  const { subscribe, update } = writable<Notification[]>([]);

  const add = (notification: Omit<Notification, 'id' | 'timestamp'>) => {
    const newNotification: Notification = {
      ...notification,
      id: crypto.randomUUID(),
      timestamp: new Date(),
      duration: notification.duration ?? 5000
    };

    update(notifications => [...notifications, newNotification]);

    // Auto-remove after duration
    if (newNotification.duration > 0) {
      setTimeout(() => {
        remove(newNotification.id);
      }, newNotification.duration);
    }

    return newNotification.id;
  };

  const remove = (id: string) => {
    update(notifications => notifications.filter(n => n.id !== id));
  };

  const clear = () => {
    update(() => []);
  };

  return {
    subscribe,
    add,
    remove,
    clear,

    // Convenience methods for different types
    success: (title: string, message?: string, duration?: number) =>
      add({ type: 'success', title, message, duration }),

    error: (title: string, message?: string, duration?: number) =>
      add({ type: 'error', title, message, duration: duration ?? 0 }), // Errors don't auto-dismiss by default

    warning: (title: string, message?: string, duration?: number) =>
      add({ type: 'warning', title, message, duration }),

    info: (title: string, message?: string, duration?: number) =>
      add({ type: 'info', title, message, duration })
  };
}

export const notificationStore = createNotificationStore();
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "notifications.ts").write_text(notifications_store)

        # Create global store
        global_store = '''import { writable } from 'svelte/store';

interface GlobalState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: Notification[];
  user: User | null;
  loading: boolean;
}

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  timestamp: Date;
}

interface User {
  id: string;
  name: string;
  email?: string;
}

// Create the global store
function createGlobalStore() {
  const { subscribe, set, update } = writable<GlobalState>({
    theme: 'light',
    sidebarOpen: false,
    notifications: [],
    user: null,
    loading: false
  });

  return {
    subscribe,

    // Theme management
    setTheme: (theme: 'light' | 'dark') => {
      update(state => ({ ...state, theme }));
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem('theme', theme);
      }
    },

    toggleTheme: () => {
      update(state => ({
        ...state,
        theme: state.theme === 'light' ? 'dark' : 'light'
      }));
    },

    // Sidebar management
    setSidebarOpen: (open: boolean) => {
      update(state => ({ ...state, sidebarOpen: open }));
    },

    toggleSidebar: () => {
      update(state => ({ ...state, sidebarOpen: !state.sidebarOpen }));
    },

    // Notification management
    addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => {
      const newNotification: Notification = {
        ...notification,
        id: crypto.randomUUID(),
        timestamp: new Date()
      };

      update(state => ({
        ...state,
        notifications: [...state.notifications, newNotification]
      }));

      // Auto-remove after 5 seconds
      setTimeout(() => {
        update(state => ({
          ...state,
          notifications: state.notifications.filter(n => n.id !== newNotification.id)
        }));
      }, 5000);
    },

    removeNotification: (id: string) => {
      update(state => ({
        ...state,
        notifications: state.notifications.filter(n => n.id !== id)
      }));
    },

    clearNotifications: () => {
      update(state => ({ ...state, notifications: [] }));
    },

    // User management
    setUser: (user: User | null) => {
      update(state => ({ ...state, user }));
    },

    // Loading state
    setLoading: (loading: boolean) => {
      update(state => ({ ...state, loading }));
    },

    // Reset store
    reset: () => {
      set({
        theme: 'light',
        sidebarOpen: false,
        notifications: [],
        user: null,
        loading: false
      });
    }
  };
}

export const globalStore = createGlobalStore();

// Helper functions for common notification types
export const notify = {
  success: (message: string) => globalStore.addNotification({ type: 'success', message }),
  error: (message: string) => globalStore.addNotification({ type: 'error', message }),
  warning: (message: string) => globalStore.addNotification({ type: 'warning', message }),
  info: (message: string) => globalStore.addNotification({ type: 'info', message })
};
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "global.ts").write_text(global_store)

    def create_composables(self) -> None:
        """Create all Svelte composables for reusable logic."""
        # Create auth composable/hook
        auth_composable = '''// Authentication composable using Svelte 5 runes
import { authState, initAuth, login, register, logout, updateProfile, clearError } from '$lib/stores/auth.svelte';

// Helper function for components that need auth functionality
export function useAuth() {
  // Initialize auth on first use
  initAuth();

  return {
    // Direct access to reactive state object properties
    get user() { return authState.user; },
    get isAuthenticated() { return authState.isAuthenticated; },
    get isLoading() { return authState.isLoading; },
    get error() { return authState.error; },
    
    // Access to the entire state object for reactive binding
    state: authState,
    
    // Actions
    login,
    register,
    logout,
    updateProfile,
    clearError
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useAuth.ts").write_text(auth_composable)
        
    def create_stores_and_composables(self) -> None:
        """Create all stores and composables."""
        print("    Creating Svelte stores and composables...")
        
        # Create stores directory and stores
        (self.frontend_dir / "src" / "lib" / "stores").mkdir(parents=True, exist_ok=True)
        self.create_svelte_stores()
        
        # Create composables directory and composables
        (self.frontend_dir / "src" / "lib" / "composables").mkdir(parents=True, exist_ok=True)
        self.create_composables()
        
        print("    ✓ Svelte stores and composables created")