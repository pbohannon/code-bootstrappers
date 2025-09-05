"""
Vue frontend generator for monorepo bootstrap.
"""

import json
from pathlib import Path
from typing import Dict, Any


class VueFrontendGenerator:
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features

    def create_structure(self):
        """Create a Vue 3 frontend with TypeScript, Pinia, and Vue Router."""
        print("  🎨 Creating Vue 3 frontend structure...")

        # package.json for Vue 3
        package_json = self._get_package_json()
        (self.project_dir / "frontend" / "package.json").write_text(
            json.dumps(package_json, indent=2)
        )

        # TypeScript configs
        tsconfig = self._get_tsconfig()
        (self.project_dir / "frontend" / "tsconfig.json").write_text(
            json.dumps(tsconfig, indent=2)
        )

        tsconfig_app = self._get_tsconfig_app()
        (self.project_dir / "frontend" / "tsconfig.app.json").write_text(
            json.dumps(tsconfig_app, indent=2)
        )

        tsconfig_node = self._get_tsconfig_node()
        (self.project_dir / "frontend" / "tsconfig.node.json").write_text(
            json.dumps(tsconfig_node, indent=2)
        )

        # Vite config
        vite_config = self._get_vite_config()
        (self.project_dir / "frontend" / "vite.config.ts").write_text(vite_config)

        # env.d.ts for TypeScript
        env_d_ts = self._get_env_d_ts()
        (self.project_dir / "frontend" / "env.d.ts").write_text(env_d_ts)

        # Main App.vue
        app_vue = self._get_app_vue()
        (self.project_dir / "frontend" / "src" / "App.vue").write_text(app_vue)

        # main.ts entry point
        main_ts = self._get_main_ts()
        (self.project_dir / "frontend" / "src" / "main.ts").write_text(main_ts)

        # Router setup
        router_ts = self._get_router()
        (self.project_dir / "frontend" / "src" / "router" / "index.ts").write_text(router_ts)

        # Pinia auth store
        auth_store = self._get_auth_store()
        (self.project_dir / "frontend" / "src" / "stores" / "auth.ts").write_text(auth_store)

        # API service
        api_service = self._get_api_service()
        (self.project_dir / "frontend" / "src" / "services" / "api.ts").write_text(api_service)

        # Types definition
        types_index = self._get_types()
        (self.project_dir / "frontend" / "src" / "types" / "index.ts").write_text(types_index)

        # Sample HomeView component
        home_view = self._get_home_view()
        (self.project_dir / "frontend" / "src" / "views" / "HomeView.vue").write_text(home_view)

        # LoginView component
        login_view = self._get_login_view()
        (self.project_dir / "frontend" / "src" / "views" / "LoginView.vue").write_text(login_view)

        # Basic CSS
        main_css = self._get_main_css()
        (self.project_dir / "frontend" / "src" / "assets" / "main.css").write_text(main_css)

        # Create placeholder for other views
        dashboard_view = self._get_dashboard_view()
        (self.project_dir / "frontend" / "src" / "views" / "DashboardView.vue").write_text(dashboard_view)

        about_view = self._get_about_view()
        (self.project_dir / "frontend" / "src" / "views" / "AboutView.vue").write_text(about_view)

        # Frontend .env.example
        frontend_env = self._get_env_example()
        (self.project_dir / "frontend" / ".env.example").write_text(frontend_env)

        # ESLint config with architectural boundaries
        eslint_config = self._get_eslint_config()
        (self.project_dir / "frontend" / ".eslintrc.js").write_text(eslint_config)

        # index.html
        index_html = self._get_index_html()
        (self.project_dir / "frontend" / "index.html").write_text(index_html)

        print("  ✓ Vue 3 frontend structure created with TypeScript, Pinia, and Vue Router")

    def _get_package_json(self) -> Dict[str, Any]:
        return {
            "name": f"{self.project_name}-frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "vite",
                "build": "run-p type-check build-only",
                "preview": "vite preview",
                "build-only": "vite build",
                "type-check": "vue-tsc --noEmit -p tsconfig.app.json --composite false",
                "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore",
                "format": "prettier --write src/",
                "test": "vitest",
                "test:unit": "vitest --environment jsdom --root src/",
                "test:e2e": "playwright test"
            },
            "dependencies": {
                "vue": "^3.4.0",
                "vue-router": "^4.2.5",
                "pinia": "^2.1.7",
                "axios": "^1.6.0",
                "@vueuse/core": "^10.7.0",
                "vee-validate": "^4.12.0",
                "yup": "^1.3.0"
            },
            "devDependencies": {
                "@rushstack/eslint-patch": "^1.3.3",
                "@tsconfig/node20": "^20.1.2",
                "@types/jsdom": "^21.1.6",
                "@types/node": "^20.10.0",
                "@vitejs/plugin-vue": "^4.5.0",
                "@vue/eslint-config-prettier": "^8.0.0",
                "@vue/eslint-config-typescript": "^12.0.0",
                "@vue/test-utils": "^2.4.3",
                "@vue/tsconfig": "^0.5.0",
                "eslint": "^8.49.0",
                "eslint-plugin-vue": "^9.17.0",
                "eslint-plugin-import": "^2.29.0",
                "eslint-plugin-boundaries": "^4.0.0",
                "jsdom": "^23.0.0",
                "npm-run-all2": "^6.1.0",
                "prettier": "^3.0.3",
                "typescript": "~5.3.0",
                "vite": "^5.0.0",
                "vitest": "^1.0.0",
                "vue-tsc": "^1.8.25"
            }
        }

    def _get_tsconfig(self) -> Dict[str, Any]:
        return {
            "compilerOptions": {
                "target": "ES2020",
                "jsx": "preserve",
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"]
                }
            },
            "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
            "exclude": ["node_modules", "dist"],
            "references": [
                {"path": "./tsconfig.node.json"},
                {"path": "./tsconfig.app.json"}
            ]
        }

    def _get_tsconfig_app(self) -> Dict[str, Any]:
        return {
            "extends": "@vue/tsconfig/tsconfig.dom.json",
            "include": ["env.d.ts", "src/**/*", "src/**/*.vue"],
            "exclude": ["src/**/__tests__/*"],
            "compilerOptions": {
                "composite": True,
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"]
                }
            }
        }

    def _get_tsconfig_node(self) -> Dict[str, Any]:
        return {
            "extends": "@tsconfig/node20/tsconfig.json",
            "include": [
                "vite.config.*",
                "vitest.config.*",
                "cypress.config.*",
                "nightwatch.conf.*",
                "playwright.config.*"
            ],
            "compilerOptions": {
                "composite": True,
                "module": "ESNext",
                "moduleResolution": "Bundler",
                "types": ["node"]
            }
        }

    def _get_vite_config(self) -> str:
        return '''import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
'''

    def _get_env_d_ts(self) -> str:
        return '''/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_NAME: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
'''

    def _get_app_vue(self) -> str:
        return '''<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Check if user is already authenticated
  await authStore.checkAuth()
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
'''

    def _get_main_ts(self) -> str:
        return '''import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
'''

    def _get_router(self) -> str:
        return '''import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    }
  ]
})

// Navigation guard for protected routes
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
'''

    def _get_auth_store(self) -> str:
        return '''import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'
import type { User, LoginCredentials, AuthTokens } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!tokens.value?.access_token)
  const currentUser = computed(() => user.value)

  // Actions
  async function login(credentials: LoginCredentials) {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiService.post<AuthTokens>('/auth/login', credentials)
      tokens.value = response
      
      // Store token in localStorage
      localStorage.setItem('access_token', response.access_token)
      
      // Fetch user profile
      await fetchProfile()
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    user.value = null
    tokens.value = null
    localStorage.removeItem('access_token')
  }

  async function fetchProfile() {
    try {
      const response = await apiService.get<User>('/users/me')
      user.value = response
    } catch (err) {
      console.error('Failed to fetch user profile:', err)
    }
  }

  async function checkAuth() {
    const token = localStorage.getItem('access_token')
    if (token) {
      tokens.value = { access_token: token, token_type: 'bearer' } as AuthTokens
      await fetchProfile()
    }
  }

  return {
    // State
    user: computed(() => user.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    
    // Getters
    isAuthenticated,
    currentUser,
    
    // Actions
    login,
    logout,
    fetchProfile,
    checkAuth
  }
})
'''

    def _get_api_service(self) -> str:
        return '''import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import router from '@/router'

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || '/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor for auth
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Handle token expiration
          localStorage.removeItem('access_token')
          await router.push({ name: 'login' })
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

export const apiService = new ApiService()
'''

    def _get_types(self) -> str:
        return '''/**
 * Type definitions for the frontend application.
 * Auto-generated types from backend will be in api.generated.ts
 */

export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface AuthTokens {
  access_token: string
  refresh_token?: string
  token_type: string
  expires_in?: number
}

export interface ApiError {
  detail: string
  status?: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
}
'''

    def _get_home_view(self) -> str:
        return '''<template>
  <div class="home">
    <h1>Welcome to {{ appName }}</h1>
    <p>
      This is your Vue 3 + TypeScript frontend connected to FastAPI backend.
    </p>
    
    <div v-if="authStore.isAuthenticated" class="user-info">
      <h2>Hello, {{ authStore.currentUser?.username }}!</h2>
      <button @click="handleLogout">Logout</button>
    </div>
    
    <div v-else class="auth-prompt">
      <p>Please <router-link to="/login">login</router-link> to continue</p>
    </div>
    
    <div class="stats">
      <h3>System Status</h3>
      <p>Backend API: <span :class="apiStatus">{{ apiStatus }}</span></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { apiService } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const appName = import.meta.env.VITE_APP_NAME || 'Vue + FastAPI App'
const apiStatus = ref<'checking' | 'online' | 'offline'>('checking')

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

const checkApiStatus = async () => {
  try {
    await apiService.get('/health')
    apiStatus.value = 'online'
  } catch {
    apiStatus.value = 'offline'
  }
}

onMounted(() => {
  checkApiStatus()
})
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.user-info {
  margin: 2rem 0;
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 8px;
}

.auth-prompt {
  margin: 2rem 0;
  padding: 1rem;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
}

.stats {
  margin-top: 2rem;
}

.online {
  color: green;
}

.offline {
  color: red;
}

.checking {
  color: orange;
}

button {
  background: #42b883;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #35a372;
}
</style>
'''

    def _get_login_view(self) -> str:
        return '''<template>
  <div class="login-container">
    <form @submit.prevent="handleSubmit" class="login-form">
      <h2>Login</h2>
      
      <div v-if="authStore.error" class="error">
        {{ authStore.error }}
      </div>
      
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="credentials.email"
          type="email"
          required
          placeholder="your@email.com"
        />
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="credentials.password"
          type="password"
          required
          placeholder="••••••••"
        />
      </div>
      
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { LoginCredentials } from '@/types'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const credentials = ref<LoginCredentials>({
  email: '',
  password: ''
})

const handleSubmit = async () => {
  const success = await authStore.login(credentials.value)
  if (success) {
    const redirect = route.query.redirect as string || '/dashboard'
    router.push(redirect)
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-form h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #42b883;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #35a372;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>
'''

    def _get_main_css(self) -> str:
        return '''/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: #f5f5f5;
  color: #333;
}

a {
  color: #42b883;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
'''

    def _get_dashboard_view(self) -> str:
        return '''<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p>Welcome to your dashboard, {{ authStore.currentUser?.username }}!</p>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}
</style>
'''

    def _get_about_view(self) -> str:
        return '''<template>
  <div class="about">
    <h1>About</h1>
    <p>This is a Vue 3 + TypeScript + FastAPI monorepo application.</p>
  </div>
</template>

<style scoped>
.about {
  padding: 2rem;
}
</style>
'''

    def _get_env_example(self) -> str:
        return '''# Frontend Environment Variables
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Vue FastAPI Monorepo
'''

    def _get_eslint_config(self) -> str:
        return '''module.exports = {
  root: true,
  env: { browser: true, es2020: true, node: true },
  extends: [
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
    'plugin:vue/vue3-essential',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:boundaries/recommended'
  ],
  overrides: [
    {
      files: ['cypress/e2e/**/*.{cy,spec}.{js,ts,jsx,tsx}'],
      extends: ['plugin:cypress/recommended']
    }
  ],
  parserOptions: {
    ecmaVersion: 'latest'
  },
  plugins: ['import', 'boundaries'],
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
    },
    'boundaries/elements': [
      {
        type: 'components',
        pattern: 'src/components/*',
        mode: 'folder'
      },
      {
        type: 'views', 
        pattern: 'src/views/*',
        mode: 'folder'
      },
      {
        type: 'services',
        pattern: 'src/services/*',
        mode: 'folder'
      },
      {
        type: 'stores',
        pattern: 'src/stores/*', 
        mode: 'folder'
      },
      {
        type: 'composables',
        pattern: 'src/composables/*',
        mode: 'folder'
      }
    ],
    'boundaries/ignore': ['**/*.test.{ts,js}', '**/*.spec.{ts,js}']
  },
  rules: {
    // Prevent direct API imports in components
    'no-restricted-imports': [
      'error',
      {
        'paths': [
          {
            'name': 'axios',
            'message': 'Use the ApiService from services/api.ts instead'
          }
        ],
        'patterns': [
          {
            'group': ['**/services/api'],
            'importNames': ['axios', 'fetch'],
            'message': 'Components should use composables or higher-level services for API calls'
          }
        ]
      }
    ],

    // Architectural boundaries for Vue
    'boundaries/element-types': [
      'error',
      {
        'default': 'disallow',
        'rules': [
          {
            'from': ['components'],
            'allow': ['components', 'composables', 'services'],
            'disallow': ['stores', 'views']
          },
          {
            'from': ['views'],
            'allow': ['components', 'composables', 'services', 'stores']
          },
          {
            'from': ['composables'],
            'allow': ['services', 'stores']
          },
          {
            'from': ['services'],
            'allow': ['services']
          },
          {
            'from': ['stores'],
            'allow': ['services']
          }
        ]
      }
    ],
    
    // Import organization
    'import/order': [
      'error',
      {
        'groups': [
          'builtin',
          'external', 
          'internal',
          'parent',
          'sibling',
          'index'
        ],
        'newlines-between': 'always',
        'alphabetize': {
          'order': 'asc',
          'caseInsensitive': true
        }
      }
    ],
    
    // Vue-specific rules
    'vue/multi-word-component-names': 'off', // Allow single word component names
    'vue/no-unused-vars': 'error'
  }
}
'''

    def _get_index_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue + FastAPI App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
'''