"""
Base frontend generator for monorepo bootstrap.
Provides common functionality and reduces code duplication across React, Vue, and Svelte generators.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseFrontendGenerator(ABC):
    """
    Base class for frontend generators that provides common functionality
    and reduces massive code duplication across framework-specific generators.
    """
    
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features
        self.frontend_dir = project_dir / "frontend"
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.framework_templates_dir = Path(__file__).parent / "templates"
    
    def create_structure(self):
        """Create the complete frontend structure."""
        print(f"  🎨 Creating {self.get_framework_name()} frontend structure...")
        
        # Create base directory structure
        self._create_base_directory_structure()
        
        # Create configuration files
        self._create_configuration_files()
        
        # Create API service and utilities
        self._create_api_service()
        
        # Create framework-specific components and routing
        self.create_framework_routes()
        self.create_framework_components()
        
        # Create testing setup if enabled
        if self.features.testing:
            self._create_base_testing_setup()
            self.create_framework_tests()
        
        print(f"  ✓ {self.get_framework_name()} frontend structure created")
    
    def _create_base_directory_structure(self):
        """Create common directory structure for all frameworks."""
        directories = [
            "frontend/src",
            "frontend/src/services",
            "frontend/src/types",
            "frontend/src/utils",
            "frontend/public",
        ]
        
        # Add framework-specific directories
        directories.extend(self.get_framework_directories())
        
        for directory in directories:
            (self.project_dir / directory).mkdir(parents=True, exist_ok=True)
    
    def _create_configuration_files(self):
        """Create all configuration files."""
        # Package.json
        package_json = self._get_base_package_json()
        (self.frontend_dir / "package.json").write_text(
            json.dumps(package_json, indent=2)
        )
        
        # TypeScript configuration
        tsconfig = self._get_base_tsconfig()
        (self.frontend_dir / "tsconfig.json").write_text(
            json.dumps(tsconfig, indent=2)
        )
        
        # Vite configuration
        vite_config = self._get_base_vite_config()
        (self.frontend_dir / "vite.config.ts").write_text(vite_config)
        
        # ESLint configuration
        if not self.features.minimal_tooling:
            eslint_config = self._get_base_eslint_config()
            (self.frontend_dir / ".eslintrc.cjs").write_text(eslint_config)
        
        # Environment example
        env_example = self._get_base_env_example()
        (self.frontend_dir / ".env.example").write_text(env_example)
        
        # Framework-specific configs
        self.create_framework_configs()
    
    def _get_base_package_json(self) -> Dict[str, Any]:
        """Generate base package.json with common structure."""
        base_scripts = {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview",
        }
        
        # Add framework-specific scripts
        framework_scripts = self.get_framework_scripts()
        base_scripts.update(framework_scripts)
        
        # Add testing scripts if enabled
        if self.features.testing:
            base_scripts.update({
                "test": "vitest",
                "test:ui": "vitest --ui",
                "test:coverage": "vitest --coverage"
            })
        
        # Add linting/formatting scripts if not minimal
        if not self.features.minimal_tooling:
            base_scripts.update({
                "lint": self.get_lint_command(),
                "lint:fix": self.get_lint_fix_command(),
                "format": "prettier --write 'src/**/*.{ts,tsx,js,jsx,vue,svelte,css,md}'",
                "format:check": "prettier --check 'src/**/*.{ts,tsx,js,jsx,vue,svelte,css,md}'"
            })
        
        # Base dependencies common to all frameworks
        base_dependencies = {
            "axios": "^1.6.0",
            "zod": "^3.22.0",
        }
        
        # Add framework-specific dependencies
        framework_deps = self.get_framework_dependencies()
        base_dependencies.update(framework_deps)
        
        # Base dev dependencies
        base_dev_dependencies = {
            "@types/node": "^20.0.0",
            "@typescript-eslint/eslint-plugin": "^8.0.0",
            "@typescript-eslint/parser": "^8.0.0",
            "typescript": "^5.3.0",
            "vite": "^5.0.0",
        }
        
        # Add framework-specific dev dependencies
        framework_dev_deps = self.get_framework_dev_dependencies()
        base_dev_dependencies.update(framework_dev_deps)
        
        # Add testing dependencies if enabled
        if self.features.testing:
            base_dev_dependencies.update({
                "vitest": "^2.0.0",
                "@testing-library/jest-dom": "^6.0.0",
                "@testing-library/user-event": "^14.0.0",
                "jsdom": "^25.0.0",
                "@vitest/ui": "^2.0.0",
                "@vitest/coverage-v8": "^2.0.0"
            })
            
            # Add framework-specific testing deps
            test_deps = self.get_framework_test_dependencies()
            base_dev_dependencies.update(test_deps)
        
        # Add linting dependencies if not minimal
        if not self.features.minimal_tooling:
            base_dev_dependencies.update({
                "eslint": "^8.57.0",
                "eslint-config-prettier": "^9.0.0",
                "prettier": "^3.0.0",
                "eslint-plugin-import": "^2.29.0",
                "eslint-plugin-boundaries": "^4.0.0"
            })
            
            # Add framework-specific linting deps
            lint_deps = self.get_framework_lint_dependencies()
            base_dev_dependencies.update(lint_deps)
        
        # Add type generation dependencies if enabled
        if self.features.type_generation:
            base_dev_dependencies.update({
                "json-schema-to-typescript": "^13.1.0"
            })
        
        return {
            "name": f"{self.project_name}-frontend",
            "version": "0.1.0",
            "private": True,
            "type": "module",
            "scripts": base_scripts,
            "dependencies": base_dependencies,
            "devDependencies": base_dev_dependencies
        }
    
    def _get_base_tsconfig(self) -> Dict[str, Any]:
        """Generate base TypeScript configuration."""
        base_config = {
            "compilerOptions": {
                "target": "ES2020",
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
                    "@/*": ["src/*"],
                    "@/types/*": ["src/types/*"],
                    "@/services/*": ["src/services/*"],
                    "@/utils/*": ["src/utils/*"]
                }
            },
            "include": ["src"]
        }
        
        # Apply framework-specific customizations
        self.customize_tsconfig(base_config)
        
        return base_config
    
    def _get_base_vite_config(self) -> str:
        """Generate base Vite configuration."""
        framework_plugin_import = self.get_vite_plugin_import()
        framework_plugin_usage = self.get_vite_plugin_usage()
        
        config = f'''import {{ defineConfig }} from 'vite'
{framework_plugin_import}
import path from 'path'

export default defineConfig({{
  plugins: [{framework_plugin_usage}],
  resolve: {{
    alias: {{
      '@': path.resolve(__dirname, './src'),
    }},
  }},
  server: {{
    port: 3000,
    proxy: {{
      '/api': {{
        target: 'http://localhost:8000',
        changeOrigin: true,
      }},
    }},
  }},'''
        
        # Testing config is now in separate vitest.config.ts file
        
        config += '\n})'
        
        return config
    
    def _get_base_eslint_config(self) -> str:
        """Generate base ESLint configuration."""
        framework_extends = self.get_eslint_framework_extends()
        framework_plugins = self.get_eslint_framework_plugins()
        framework_rules = self.get_eslint_framework_rules()
        boundary_patterns = self.get_eslint_boundary_patterns()
        
        return f'''module.exports = {{
  root: true,
  env: {{ browser: true, es2020: true }},
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:boundaries/recommended',{framework_extends}
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['import', 'boundaries'{framework_plugins}],
  settings: {{
    'import/resolver': {{
      typescript: {{
        alwaysTryTypes: true,
        project: './tsconfig.json',
      }},
    }},
    'boundaries/elements': [{boundary_patterns}
    ],
    'boundaries/ignore': ['**/*.test.{{ts,tsx,js,jsx,vue,svelte}}', '**/*.spec.{{ts,tsx,js,jsx,vue,svelte}}']
  }},
  rules: {{
    // Prevent direct API imports in components
    'no-restricted-imports': [
      'error',
      {{
        'paths': [
          {{
            'name': 'axios',
            'message': 'Use the ApiService from services/api.ts instead'
          }}
        ]
      }}
    ],

    // Import organization
    'import/order': [
      'error',
      {{
        'groups': [
          'builtin',
          'external', 
          'internal',
          'parent',
          'sibling',
          'index'
        ],
        'newlines-between': 'always',
        'alphabetize': {{
          'order': 'asc',
          'caseInsensitive': true
        }}
      }}
    ],
    
    '@typescript-eslint/no-unused-vars': ['error', {{ argsIgnorePattern: '^_' }}],{framework_rules}
  }},
}}'''
    
    def _get_base_env_example(self) -> str:
        """Generate base environment example file."""
        env_fallback = f'''# Frontend Environment Variables
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME={self.project_name.replace('_', ' ').title()} App
VITE_ENVIRONMENT=development
'''
        # Try to use template, fallback to hardcoded
        try:
            return self.load_template("env-example")
        except FileNotFoundError:
            return env_fallback
    
    def _create_api_service(self):
        """Create common API service from template or fallback."""
        api_service_fallback = '''import axios from 'axios';
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
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
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
        self.create_from_hardcoded_or_template(
            "api-service",
            self.frontend_dir / "src" / "services" / "api.ts",
            api_service_fallback
        )
    
    def _create_base_testing_setup(self):
        """Create base testing setup using unified template."""
        self.create_from_hardcoded_or_template(
            "frontend/test-setup.ts",
            self.frontend_dir / "src" / "utils" / "test-setup.ts",
            '''import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock environment variables
vi.stubEnv('VITE_API_URL', 'http://localhost:8000/api/v1')
vi.stubEnv('VITE_APP_NAME', 'Test App')

// Mock localStorage
Object.defineProperty(window, 'localStorage', {
  value: {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  },
  writable: true,
})

// Mock crypto.randomUUID for environments that don't support it
if (!globalThis.crypto?.randomUUID) {
  Object.defineProperty(globalThis, 'crypto', {
    value: {
      randomUUID: () => `test-uuid-${Math.random().toString(36).substring(7)}`
    }
  })
}

// Setup global test utilities
(globalThis as any).testUtils = {
  waitFor: (callback: () => boolean, timeout = 1000) => {
    return new Promise<void>((resolve, reject) => {
      const startTime = Date.now()
      const check = () => {
        if (callback()) {
          resolve()
        } else if (Date.now() - startTime > timeout) {
          reject(new Error('Timeout waiting for condition'))
        } else {
          setTimeout(check, 50)
        }
      }
      check()
    })
  }
}'''
        )
        
        # Create unified Vitest config using template system
        self._create_vitest_config()
    
    def _create_vitest_config(self):
        """Create unified Vitest configuration for all frameworks."""
        # Get framework-specific template variables
        framework_imports = self.get_vite_plugin_import()
        framework_plugins = self.get_vite_plugin_usage()
        file_extensions = self.get_test_file_extensions()
        
        self.write_from_template(
            "frontend/vitest.config.ts",
            self.frontend_dir / "vitest.config.ts",
            framework_imports=framework_imports,
            framework_plugins=framework_plugins,
            file_extensions=file_extensions
        )
    
    def load_template(self, template_name: str, **kwargs) -> str:
        """
        Load a template file and perform variable substitution.
        
        Args:
            template_name: Name of the template file (without .template extension)
            **kwargs: Variables to substitute in the template
            
        Returns:
            Template content with variables substituted
        """
        template_path = self.templates_dir / f"{template_name}.template"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        template_content = template_path.read_text()
        
        # Add common template variables
        template_vars = {
            'project_name': self.project_name,
            'project_title': self.project_name.replace('_', ' ').title(),
            'framework_name': self.get_framework_name(),
            'framework_name_lower': self.get_framework_name().lower(),
            **kwargs
        }
        
        # Simple template substitution
        for key, value in template_vars.items():
            template_content = template_content.replace(f'{{{{{key}}}}}', str(value))
        
        return template_content
    
    def write_from_template(self, template_name: str, output_path: Path, **kwargs) -> None:
        """
        Load a template and write it to the specified output path.
        
        Args:
            template_name: Name of the template file
            output_path: Path where the rendered template should be written
            **kwargs: Variables to substitute in the template
        """
        content = self.load_template(template_name, **kwargs)
        output_path.write_text(content)
    
    def create_from_hardcoded_or_template(self, 
                                          template_name: str, 
                                          output_path: Path, 
                                          fallback_content: str, 
                                          **kwargs) -> None:
        """
        Create a file from template if available, otherwise use hardcoded content.
        This allows for gradual migration from hardcoded strings to templates.
        
        Args:
            template_name: Name of the template file to try
            output_path: Path where the content should be written
            fallback_content: Hardcoded content to use if template doesn't exist
            **kwargs: Variables to substitute in the template
        """
        template_path = self.templates_dir / f"{template_name}.template"
        
        if template_path.exists():
            self.write_from_template(template_name, output_path, **kwargs)
        else:
            output_path.write_text(fallback_content)
    
    # Abstract methods that must be implemented by framework-specific generators
    
    @abstractmethod
    def get_framework_name(self) -> str:
        """Return the name of the framework (e.g., 'React', 'Vue', 'Svelte')."""
        pass
    
    @abstractmethod
    def get_framework_directories(self) -> List[str]:
        """Return framework-specific directory paths to create."""
        pass
    
    @abstractmethod
    def get_framework_dependencies(self) -> Dict[str, str]:
        """Return framework-specific runtime dependencies."""
        pass
    
    @abstractmethod
    def get_framework_dev_dependencies(self) -> Dict[str, str]:
        """Return framework-specific development dependencies."""
        pass
    
    @abstractmethod
    def get_framework_scripts(self) -> Dict[str, str]:
        """Return framework-specific npm scripts."""
        pass
    
    @abstractmethod
    def get_vite_plugin_import(self) -> str:
        """Return the import statement for framework's Vite plugin."""
        pass
    
    @abstractmethod
    def get_vite_plugin_usage(self) -> str:
        """Return the usage of framework's Vite plugin."""
        pass
    
    @abstractmethod
    def customize_tsconfig(self, config: Dict[str, Any]) -> None:
        """Customize TypeScript configuration for the framework."""
        pass
    
    @abstractmethod
    def get_eslint_framework_extends(self) -> str:
        """Return framework-specific ESLint extends configuration."""
        pass
    
    @abstractmethod
    def get_eslint_framework_plugins(self) -> str:
        """Return framework-specific ESLint plugins."""
        pass
    
    @abstractmethod
    def get_eslint_framework_rules(self) -> str:
        """Return framework-specific ESLint rules."""
        pass
    
    @abstractmethod
    def get_eslint_boundary_patterns(self) -> str:
        """Return framework-specific boundary patterns for ESLint."""
        pass
    
    @abstractmethod
    def get_lint_command(self) -> str:
        """Return the lint command for this framework."""
        pass
    
    @abstractmethod
    def get_lint_fix_command(self) -> str:
        """Return the lint fix command for this framework."""
        pass
    
    @abstractmethod
    def get_test_file_extensions(self) -> str:
        """Return framework-specific test file extensions (e.g., ',tsx' for React, '.vue' for Vue)."""
        pass
    
    @abstractmethod
    def create_framework_routes(self) -> None:
        """Create framework-specific routing setup."""
        pass
    
    @abstractmethod
    def create_framework_components(self) -> None:
        """Create framework-specific starter components."""
        pass
    
    @abstractmethod
    def create_framework_configs(self) -> None:
        """Create framework-specific configuration files."""
        pass
    
    # Template loading and substitution methods
    
    def load_framework_template(self, template_path: str, **kwargs) -> str:
        """Load a framework-specific template file and return its contents."""
        framework_name = self.get_framework_name().lower()
        full_path = self.framework_templates_dir / framework_name / template_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Template not found: {full_path}")
        
        content = full_path.read_text()
        
        # Apply substitutions if any kwargs are provided
        if kwargs:
            for key, value in kwargs.items():
                content = content.replace(f'{{{{{key}}}}}', str(value))
                
        return content
    
    def substitute_template_vars(self, content: str) -> str:
        """Replace template variables with actual values."""
        substitutions = {
            '{{PROJECT_TITLE}}': self.project_name.replace('_', ' ').title(),
            '{{PROJECT_NAME}}': self.project_name,
            '{{APP_NAME}}': self.project_name.replace('_', ' ').title(),
        }
        
        result = content
        for placeholder, value in substitutions.items():
            result = result.replace(placeholder, value)
        
        return result
    
    def load_and_substitute_template(self, template_path: str) -> str:
        """Load a template and apply variable substitutions."""
        content = self.load_framework_template(template_path)
        return self.substitute_template_vars(content)

    # Optional methods with default implementations
    
    def get_framework_test_dependencies(self) -> Dict[str, str]:
        """Return framework-specific test dependencies. Override if needed."""
        return {}
    
    def get_framework_lint_dependencies(self) -> Dict[str, str]:
        """Return framework-specific linting dependencies. Override if needed."""
        return {}
    
    def create_framework_tests(self) -> None:
        """Create framework-specific test examples. Override if needed."""
        pass