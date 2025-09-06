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
        # Create auth store
        auth_store = '''import { writable, derived, get } from 'svelte/store';
import type { User, LoginCredentials, RegisterData, AuthTokens } from '$types/auth.js';
import { browser } from '$app/environment';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  });

  return {
    subscribe,

    // Initialize auth state from localStorage
    init: () => {
      if (!browser) return;

      try {
        const token = localStorage.getItem('auth_token');
        const user = localStorage.getItem('auth_user');
        
        if (token && user) {
          const parsedUser = JSON.parse(user);
          set({
            user: parsedUser,
            isAuthenticated: true,
            isLoading: false,
            error: null
          });
        }
      } catch (error) {
        console.error('Failed to initialize auth state:', error);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    },

    // Login user
    login: async (credentials: LoginCredentials): Promise<boolean> => {
      update(state => ({ ...state, isLoading: true, error: null }));

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

        set({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null
        });

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Login failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    },

    // Register user
    register: async (data: RegisterData): Promise<boolean> => {
      update(state => ({ ...state, isLoading: true, error: null }));

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

        set({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null
        });

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Registration failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    },

    // Logout user
    logout: () => {
      if (browser) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
      }

      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      });
    },

    // Clear error
    clearError: () => {
      update(state => ({ ...state, error: null }));
    },

    // Update user profile
    updateProfile: async (updates: Partial<User>): Promise<boolean> => {
      const currentState = get({ subscribe });
      if (!currentState.user) return false;

      update(state => ({ ...state, isLoading: true }));

      try {
        const response = await fetch(`/api/v1/users/${currentState.user!.id}`, {
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

        update(state => ({
          ...state,
          user: updatedUser,
          isLoading: false
        }));

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Profile update failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    }
  };
}

// Create the auth store
export const authStore = createAuthStore();
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "auth.ts").write_text(auth_store)

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
        auth_composable = '''// Authentication composable using Svelte stores
import { writable, derived, get } from 'svelte/store';
import type { User, LoginCredentials, RegisterData, AuthTokens } from '$types/auth.js';
import { browser } from '$app/environment';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  });

  return {
    subscribe,

    // Initialize auth state from localStorage
    init: () => {
      if (!browser) return;

      try {
        const token = localStorage.getItem('auth_token');
        const user = localStorage.getItem('auth_user');
        
        if (token && user) {
          const parsedUser = JSON.parse(user);
          set({
            user: parsedUser,
            isAuthenticated: true,
            isLoading: false,
            error: null
          });
        }
      } catch (error) {
        console.error('Failed to initialize auth state:', error);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    },

    // Login user
    login: async (credentials: LoginCredentials): Promise<boolean> => {
      update(state => ({ ...state, isLoading: true, error: null }));

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

        set({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null
        });

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Login failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    },

    // Register user
    register: async (data: RegisterData): Promise<boolean> => {
      update(state => ({ ...state, isLoading: true, error: null }));

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

        set({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null
        });

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Registration failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    },

    // Logout user
    logout: () => {
      if (browser) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
      }

      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      });
    },

    // Clear error
    clearError: () => {
      update(state => ({ ...state, error: null }));
    },

    // Update user profile
    updateProfile: async (updates: Partial<User>): Promise<boolean> => {
      const currentState = get({ subscribe });
      if (!currentState.user) return false;

      update(state => ({ ...state, isLoading: true }));

      try {
        const response = await fetch(`/api/v1/users/${currentState.user!.id}`, {
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

        update(state => ({
          ...state,
          user: updatedUser,
          isLoading: false
        }));

        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Profile update failed';
        update(state => ({ ...state, isLoading: false, error: message }));
        return false;
      }
    }
  };
}

// Create the auth store
export const authStore = createAuthStore();

// Helper function for components
export function useAuth() {
  // Initialize on first use
  authStore.init();

  return {
    // Derived store for easy reactivity
    auth: derived(authStore, $auth => $auth),
    
    // Actions
    login: authStore.login,
    register: authStore.register,
    logout: authStore.logout,
    updateProfile: authStore.updateProfile,
    clearError: authStore.clearError
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useAuth.ts").write_text(auth_composable)

        # Create API composable
        api_composable = '''// API composable for making HTTP requests
import { writable } from 'svelte/store';
import type { ApiResponse, ApiRequestConfig } from '$types/api.js';
import { browser } from '$app/environment';

interface ApiState {
  isLoading: boolean;
  error: string | null;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

function createApiStore() {
  const { subscribe, set, update } = writable<ApiState>({
    isLoading: false,
    error: null
  });

  return {
    subscribe,
    setLoading: (loading: boolean) => update(state => ({ ...state, isLoading: loading })),
    setError: (error: string | null) => update(state => ({ ...state, error })),
    clearError: () => update(state => ({ ...state, error: null }))
  };
}

const apiStore = createApiStore();

// Generic API request function
async function request<T = unknown>(
  endpoint: string,
  config: ApiRequestConfig = {}
): Promise<ApiResponse<T>> {
  const {
    method = 'GET',
    headers = {},
    body,
    timeout = 30000
  } = config;

  apiStore.setLoading(true);
  apiStore.setError(null);

  try {
    // Get auth token from localStorage if available
    let authHeaders = {};
    if (browser) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        authHeaders = { Authorization: `Bearer ${token}` };
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...headers
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data: ApiResponse<T> = await response.json();
    return data;

  } catch (error) {
    const message = error instanceof Error ? error.message : 'API request failed';
    apiStore.setError(message);
    throw error;
  } finally {
    apiStore.setLoading(false);
  }
}

export function useApi() {
  return {
    // Store for global API state
    api: { subscribe: apiStore.subscribe },
    
    // HTTP methods
    get: <T = unknown>(endpoint: string, config?: Omit<ApiRequestConfig, 'method'>) =>
      request<T>(endpoint, { ...config, method: 'GET' }),

    post: <T = unknown>(endpoint: string, body?: unknown, config?: Omit<ApiRequestConfig, 'method' | 'body'>) =>
      request<T>(endpoint, { ...config, method: 'POST', body }),

    put: <T = unknown>(endpoint: string, body?: unknown, config?: Omit<ApiRequestConfig, 'method' | 'body'>) =>
      request<T>(endpoint, { ...config, method: 'PUT', body }),

    patch: <T = unknown>(endpoint: string, body?: unknown, config?: Omit<ApiRequestConfig, 'method' | 'body'>) =>
      request<T>(endpoint, { ...config, method: 'PATCH', body }),

    delete: <T = unknown>(endpoint: string, config?: Omit<ApiRequestConfig, 'method'>) =>
      request<T>(endpoint, { ...config, method: 'DELETE' }),

    // Utility methods
    clearError: apiStore.clearError,
    
    // Health check
    healthCheck: () => request('/health'),

    // Upload file
    upload: async <T = unknown>(endpoint: string, file: File, additionalFields?: Record<string, string>) => {
      apiStore.setLoading(true);
      apiStore.setError(null);

      try {
        const formData = new FormData();
        formData.append('file', file);

        if (additionalFields) {
          Object.entries(additionalFields).forEach(([key, value]) => {
            formData.append(key, value);
          });
        }

        let authHeaders = {};
        if (browser) {
          const token = localStorage.getItem('auth_token');
          if (token) {
            authHeaders = { Authorization: `Bearer ${token}` };
          }
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method: 'POST',
          headers: authHeaders,
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
        }

        const data: ApiResponse<T> = await response.json();
        return data;

      } catch (error) {
        const message = error instanceof Error ? error.message : 'Upload failed';
        apiStore.setError(message);
        throw error;
      } finally {
        apiStore.setLoading(false);
      }
    },

    // Batch requests
    batch: async <T = unknown>(requests: Array<{ endpoint: string; config?: ApiRequestConfig }>) => {
      const results = await Promise.allSettled(
        requests.map(({ endpoint, config }) => request<T>(endpoint, config))
      );

      return results.map((result, index) => ({
        endpoint: requests[index].endpoint,
        status: result.status,
        data: result.status === 'fulfilled' ? result.value : null,
        error: result.status === 'rejected' ? result.reason : null
      }));
    }
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useApi.ts").write_text(api_composable)

        # Create localStorage composable
        localstorage_composable = '''// LocalStorage composable for persisting data
import { writable, type Writable } from 'svelte/store';
import { browser } from '$app/environment';

export function useLocalStorage<T>(
  key: string,
  defaultValue: T,
  options: {
    serializer?: {
      read: (value: string) => T;
      write: (value: T) => string;
    };
  } = {}
): Writable<T> & { 
  reset: () => void; 
  remove: () => void; 
} {
  const serializer = options.serializer || {
    read: (v: string) => {
      try {
        return JSON.parse(v);
      } catch {
        return v as T;
      }
    },
    write: (v: T) => JSON.stringify(v)
  };

  // Get initial value from localStorage or use default
  const getStoredValue = (): T => {
    if (!browser) return defaultValue;

    try {
      const item = localStorage.getItem(key);
      if (item === null) return defaultValue;
      return serializer.read(item);
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return defaultValue;
    }
  };

  // Create the writable store with initial value
  const { subscribe, set, update } = writable<T>(getStoredValue());

  // Custom set function that also updates localStorage
  const setValue = (value: T) => {
    set(value);
    
    if (browser) {
      try {
        localStorage.setItem(key, serializer.write(value));
      } catch (error) {
        console.error(`Error setting localStorage key "${key}":`, error);
      }
    }
  };

  // Custom update function that also updates localStorage
  const updateValue = (updater: (value: T) => T) => {
    update((currentValue) => {
      const newValue = updater(currentValue);
      
      if (browser) {
        try {
          localStorage.setItem(key, serializer.write(newValue));
        } catch (error) {
          console.error(`Error updating localStorage key "${key}":`, error);
        }
      }
      
      return newValue;
    });
  };

  // Reset to default value
  const reset = () => {
    setValue(defaultValue);
  };

  // Remove from localStorage and reset to default
  const remove = () => {
    if (browser) {
      try {
        localStorage.removeItem(key);
      } catch (error) {
        console.error(`Error removing localStorage key "${key}":`, error);
      }
    }
    set(defaultValue);
  };

  // Listen for storage events from other tabs/windows
  if (browser) {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key) {
        if (e.newValue === null) {
          set(defaultValue);
        } else {
          try {
            set(serializer.read(e.newValue));
          } catch (error) {
            console.warn(`Error parsing storage event for key "${key}":`, error);
            set(defaultValue);
          }
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
  }

  return {
    subscribe,
    set: setValue,
    update: updateValue,
    reset,
    remove
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useLocalStorage.ts").write_text(localstorage_composable)

        # Create debounce composable
        debounce_composable = '''// Debounce composable for delaying function execution
import { writable, derived } from 'svelte/store';

export function useDebounce<T>(value: T, delay: number = 300) {
  const store = writable(value);
  const debouncedStore = writable(value);
  
  let timeoutId: NodeJS.Timeout | null = null;

  // Subscribe to the original store and debounce updates
  store.subscribe((newValue) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      debouncedStore.set(newValue);
      timeoutId = null;
    }, delay);
  });

  return {
    // Original value (updates immediately)
    value: store,
    
    // Debounced value (updates after delay)
    debouncedValue: { subscribe: debouncedStore.subscribe },
    
    // Set the value
    set: (newValue: T) => store.set(newValue),
    
    // Update the value
    update: (updater: (value: T) => T) => store.update(updater),
    
    // Force immediate update of debounced value
    flush: () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
      store.subscribe((currentValue) => {
        debouncedStore.set(currentValue);
      })();
    },
    
    // Cancel pending debounce
    cancel: () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
    }
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useDebounce.ts").write_text(debounce_composable)

        # Create pagination composable
        pagination_composable = '''// Pagination composable for managing paginated data
import { writable, derived } from 'svelte/store';
import type { PaginationMeta } from '$types/api.js';

export interface PaginationOptions {
  initialPage?: number;
  initialPageSize?: number;
  totalItems?: number;
}

export interface PaginationState {
  currentPage: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  startIndex: number;
  endIndex: number;
  isLoading: boolean;
}

export function usePagination(options: PaginationOptions = {}) {
  const {
    initialPage = 1,
    initialPageSize = 10,
    totalItems: initialTotalItems = 0
  } = options;

  // Core state
  const currentPage = writable(initialPage);
  const pageSize = writable(initialPageSize);
  const totalItems = writable(initialTotalItems);
  const isLoading = writable(false);

  // Derived state
  const pagination = derived(
    [currentPage, pageSize, totalItems, isLoading],
    ([$currentPage, $pageSize, $totalItems, $isLoading]) => {
      const totalPages = Math.ceil($totalItems / $pageSize);
      const hasNextPage = $currentPage < totalPages;
      const hasPreviousPage = $currentPage > 1;
      const startIndex = ($currentPage - 1) * $pageSize + 1;
      const endIndex = Math.min($currentPage * $pageSize, $totalItems);

      return {
        currentPage: $currentPage,
        pageSize: $pageSize,
        totalItems: $totalItems,
        totalPages,
        hasNextPage,
        hasPreviousPage,
        startIndex,
        endIndex,
        isLoading: $isLoading
      } as PaginationState;
    }
  );

  return {
    // State
    pagination,
    
    // Actions
    setPage: (page: number) => {
      currentPage.update(current => {
        const newPage = Math.max(1, Math.min(page, Math.ceil(totalItems as any / pageSize as any)));
        return newPage;
      });
    },

    nextPage: () => {
      currentPage.update(current => {
        const maxPage = Math.ceil(totalItems as any / pageSize as any);
        return Math.min(current + 1, maxPage);
      });
    },

    previousPage: () => {
      currentPage.update(current => Math.max(current - 1, 1));
    },

    setPageSize: (size: number) => {
      pageSize.set(Math.max(1, size));
      currentPage.set(1);
    },

    setTotalItems: (total: number) => {
      totalItems.set(Math.max(0, total));
    },

    setLoading: (loading: boolean) => {
      isLoading.set(loading);
    }
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "usePagination.ts").write_text(pagination_composable)

        # Create user data composable using Svelte 5 runes (.svelte.ts extension required)
        user_composable = '''// Svelte 5 rune-based composable - must use .svelte.ts extension
interface User {
  id: string;
  name: string;
  email?: string;
  created_at: string;
  updated_at: string;
}

export function useUserData(userId: string) {
  let user = $state<User | null>(null);
  let loading = $state(true);
  let error = $state<string | null>(null);

  async function fetchUser() {
    if (!userId) {
      user = null;
      loading = false;
      return;
    }

    try {
      loading = true;
      error = null;

      // Simulate API call - replace with actual endpoint
      // const response = await fetch(`/api/v1/users/${userId}`);
      // const userData = await response.json();

      // Mock data for demo purposes
      const userData: User = {
        id: userId,
        name: `Demo User ${userId.slice(-4)}`,
        email: `demo@example.com`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      user = userData;
    } catch (err: any) {
      error = err.detail || 'Failed to fetch user data';
      user = null;
    } finally {
      loading = false;
    }
  }

  // Effect to fetch user when userId changes
  $effect(() => {
    fetchUser();
  });

  async function updateUser(updates: Partial<User>) {
    if (!user) return;

    try {
      loading = true;
      error = null;

      // const response = await fetch(`/api/v1/users/${user.id}`, {
      //   method: 'PUT', 
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(updates)
      // });
      // const updatedUser = await response.json();

      // Mock update for demo
      const updatedUser = { ...user, ...updates, updated_at: new Date().toISOString() };
      user = updatedUser;

      return updatedUser;
    } catch (err: any) {
      error = err.detail || 'Failed to update user';
      throw err;
    } finally {
      loading = false;
    }
  }

  function refresh() {
    fetchUser();
  }

  return {
    // Reactive getters following the guide patterns
    get user() { return user; },
    get loading() { return loading; },
    get error() { return error; },

    // Actions
    updateUser,
    refresh
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "useUserData.svelte.ts").write_text(user_composable)

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


