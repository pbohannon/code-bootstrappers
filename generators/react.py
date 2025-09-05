"""
React frontend generator for monorepo bootstrap.
"""

import json
from pathlib import Path
from typing import Dict, Any


class ReactFrontendGenerator:
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features

    def create_structure(self):
        """Create React frontend structure with TypeScript."""
        print("  🎨 Creating React frontend structure...")

        # Create package.json for React
        package_json = self._get_package_json()
        (self.project_dir / "frontend" / "package.json").write_text(
            json.dumps(package_json, indent=2)
        )

        # TypeScript config
        tsconfig = self._get_tsconfig()
        (self.project_dir / "frontend" / "tsconfig.json").write_text(
            json.dumps(tsconfig, indent=2)
        )

        # Vite config
        vite_config = self._get_vite_config()
        (self.project_dir / "frontend" / "vite.config.ts").write_text(vite_config)

        # ESLint config with architectural boundaries
        eslint_config = self._get_eslint_config()
        (self.project_dir / "frontend" / ".eslintrc.js").write_text(eslint_config)

        # API service
        api_service = self._get_api_service()
        (self.project_dir / "frontend" / "src" / "services" / "api.ts").write_text(api_service)

        # Basic App component
        app_component = self._get_app_component()
        (self.project_dir / "frontend" / "src" / "App.tsx").write_text(app_component)

        # Frontend .env.example
        frontend_env = self._get_env_example()
        (self.project_dir / "frontend" / ".env.example").write_text(frontend_env)

        print("  ✓ React frontend structure created with TypeScript, Vite, and TanStack Query")

    def _get_package_json(self) -> Dict[str, Any]:
        return {
            "name": f"{self.project_name}-frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview",
                "test": "vitest",
                "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
                "format": "prettier --write 'src/**/*.{ts,tsx,css}'",
                "type-check": "tsc --noEmit"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.20.0",
                "@tanstack/react-query": "^5.0.0",
                "axios": "^1.6.0",
                "zustand": "^4.4.0",
                "react-hook-form": "^7.48.0",
                "zod": "^3.22.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "@typescript-eslint/eslint-plugin": "^6.0.0",
                "@typescript-eslint/parser": "^6.0.0",
                "@vitejs/plugin-react": "^4.2.0",
                "eslint": "^8.50.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.0",
                "eslint-plugin-import": "^2.29.0",
                "eslint-plugin-boundaries": "^4.0.0",
                "prettier": "^3.1.0",
                "typescript": "^5.3.0",
                "vite": "^5.0.0",
                "vitest": "^1.0.0",
                "@testing-library/react": "^14.0.0",
                "@testing-library/jest-dom": "^6.1.0",
                "@testing-library/user-event": "^14.5.0"
            }
        }

    def _get_tsconfig(self) -> Dict[str, Any]:
        return {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "baseUrl": ".",
                "paths": {
                    "@/*": ["src/*"],
                    "@/types/*": ["src/types/*"],
                    "@/services/*": ["src/services/*"],
                    "@/components/*": ["src/components/*"],
                    "@/hooks/*": ["src/hooks/*"],
                    "@/utils/*": ["src/utils/*"]
                }
            },
            "include": ["src"],
            "references": [{"path": "./tsconfig.node.json"}]
        }

    def _get_vite_config(self) -> str:
        return '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
'''

    def _get_eslint_config(self) -> str:
        return '''module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:boundaries/recommended'
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', 'import', 'boundaries'],
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
        type: 'pages', 
        pattern: 'src/pages/*',
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
        type: 'hooks',
        pattern: 'src/hooks/*',
        mode: 'folder'
      }
    ],
    'boundaries/ignore': ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}']
  },
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    
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
            'message': 'Components should use hooks or higher-level services for API calls'
          }
        ]
      }
    ],

    // Architectural boundaries
    'boundaries/element-types': [
      'error',
      {
        'default': 'disallow',
        'rules': [
          {
            'from': ['components'],
            'allow': ['components', 'hooks', 'services'],
            'disallow': ['stores', 'pages']
          },
          {
            'from': ['pages'],
            'allow': ['components', 'hooks', 'services', 'stores']
          },
          {
            'from': ['hooks'],
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
    
    // Prevent prop drilling indicators
    'react/prop-types': 'off', // We use TypeScript
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }]
  },
}
'''

    def _get_api_service(self) -> str:
        return '''import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig } from 'axios';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || '/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for auth
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Handle token refresh or redirect to login
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

export const apiService = new ApiService();
'''

    def _get_app_component(self) -> str:
        return f'''import {{ QueryClient, QueryClientProvider }} from '@tanstack/react-query';
import {{ BrowserRouter }} from 'react-router-dom';

const queryClient = new QueryClient({{
  defaultOptions: {{
    queries: {{
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    }},
  }},
}});

function App() {{
  return (
    <QueryClientProvider client={{queryClient}}>
      <BrowserRouter>
        <div className="App">
          <h1>Welcome to {self.project_name}</h1>
          <p>Frontend is connected to the backend API</p>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}}

export default App;
'''

    def _get_env_example(self) -> str:
        return '''# Frontend Environment Variables
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Monorepo Frontend
'''