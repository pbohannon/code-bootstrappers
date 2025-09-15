"""
Vue frontend generator for monorepo bootstrap.
Refactored to use BaseFrontendGenerator and template system.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

from .base_frontend import BaseFrontendGenerator


class VueFrontendGenerator(BaseFrontendGenerator):
    """Vue 3 frontend generator with TypeScript, Pinia, and Vue Router."""
    
    def get_framework_name(self) -> str:
        return "Vue"
    
    def get_framework_directories(self) -> List[str]:
        return [
            "frontend/src/components",
            "frontend/src/views", 
            "frontend/src/router",
            "frontend/src/stores",
            "frontend/src/assets",
        ]
    
    def get_framework_dependencies(self) -> Dict[str, str]:
        return {
            "vue": "^3.4.0",
            "vue-router": "^4.2.5",
            "pinia": "^2.1.7",
            "@vueuse/core": "^10.7.0",
            "vee-validate": "^4.12.0",
            "yup": "^1.3.0"
        }
    
    def get_framework_dev_dependencies(self) -> Dict[str, str]:
        return {
            "@rushstack/eslint-patch": "^1.3.3",
            "@tsconfig/node20": "^20.1.2",
            "@vitejs/plugin-vue": "^4.5.0",
            "@vue/eslint-config-prettier": "^8.0.0",
            "@vue/eslint-config-typescript": "^12.0.0",
            "@vue/tsconfig": "^0.5.0",
            "npm-run-all2": "^6.1.0",
            "vue-tsc": "^1.8.25"
        }
    
    def get_framework_test_dependencies(self) -> Dict[str, str]:
        return {
            "@vue/test-utils": "^2.4.3",
        }
    
    def get_framework_lint_dependencies(self) -> Dict[str, str]:
        return {
            "eslint-plugin-vue": "^9.17.0",
        }
    
    def get_framework_scripts(self) -> Dict[str, str]:
        return {
            "build": "run-p type-check build-only",
            "build-only": "vite build",
            "type-check": "vue-tsc --noEmit -p tsconfig.app.json --composite false",
        }
    
    def get_vite_plugin_import(self) -> str:
        return "import vue from '@vitejs/plugin-vue'"
    
    def get_vite_plugin_usage(self) -> str:
        return "vue()"
    
    def customize_tsconfig(self, config: Dict[str, Any]) -> None:
        """Customize TypeScript configuration for Vue."""
        # Vue needs JSX preserve and Vue types
        config["compilerOptions"]["jsx"] = "preserve"
        config["include"] = ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"]
        config["references"] = [
            {"path": "./tsconfig.node.json"},
            {"path": "./tsconfig.app.json"}
        ]
    
    def get_eslint_framework_extends(self) -> str:
        return '''
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
    'plugin:vue/vue3-essential','''
    
    def get_eslint_framework_plugins(self) -> str:
        return ", 'vue'"
    
    def get_eslint_framework_rules(self) -> str:
        return '''
    
    // Vue-specific rules
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'error','''
    
    def get_eslint_boundary_patterns(self) -> str:
        return '''
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
      }'''
    
    def get_lint_command(self) -> str:
        return "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore"
    
    def get_lint_fix_command(self) -> str:
        return "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore"
    
    def get_test_file_extensions(self) -> str:
        """Return Vue-specific test file extensions."""
        return ",.vue"
    
    def create_framework_configs(self) -> None:
        """Create Vue-specific configuration files."""
        # Vue needs additional TypeScript config files
        self._create_tsconfig_app()
        self._create_tsconfig_node() 
        self._create_env_d_ts()
        self._create_index_html()
    
    def create_framework_routes(self) -> None:
        """Create Vue Router setup."""
        router_content = self._get_router()
        (self.frontend_dir / "src" / "router" / "index.ts").write_text(router_content)
    
    def create_framework_components(self) -> None:
        """Create Vue starter components."""
        # Create stores directory for future use
        (self.frontend_dir / "src" / "stores").mkdir(exist_ok=True)
        
        # Create types
        types_content = self._get_types()
        (self.frontend_dir / "src" / "types" / "index.ts").write_text(types_content)
        
        # Create main App.vue
        app_vue = self._get_app_vue()
        (self.frontend_dir / "src" / "App.vue").write_text(app_vue)
        
        # Create main.ts entry point
        main_ts = self._get_main_ts()
        (self.frontend_dir / "src" / "main.ts").write_text(main_ts)
        
        # Create views
        views = [
            ("HomeView.vue", self._get_home_view()),
            ("AboutView.vue", self._get_about_view()),
        ]
        
        for filename, content in views:
            (self.frontend_dir / "src" / "views" / filename).write_text(content)
        
        # Create main CSS
        main_css = self._get_main_css()
        (self.frontend_dir / "src" / "assets" / "main.css").write_text(main_css)
    
    # Vue-specific configuration methods
    
    def _create_tsconfig_app(self) -> None:
        """Create Vue-specific tsconfig.app.json."""
        tsconfig_app = {
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
        (self.frontend_dir / "tsconfig.app.json").write_text(
            json.dumps(tsconfig_app, indent=2)
        )
    
    def _create_tsconfig_node(self) -> None:
        """Create Vue-specific tsconfig.node.json."""
        tsconfig_node = {
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
        (self.frontend_dir / "tsconfig.node.json").write_text(
            json.dumps(tsconfig_node, indent=2)
        )
    
    def _create_env_d_ts(self) -> None:
        """Create Vue-specific env.d.ts."""
        env_d_ts = '''/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_NAME: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
'''
        (self.frontend_dir / "env.d.ts").write_text(env_d_ts)
    
    def _create_index_html(self) -> None:
        """Create Vue-specific index.html."""
        index_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.project_name.replace('_', ' ').title()} App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
'''
        (self.frontend_dir / "index.html").write_text(index_html)
    
    # Vue component methods - keeping the original Vue-specific functionality
    
    def _get_app_vue(self) -> str:
        return '''<template>
  <div id="app">
    <router-view />
  </div>
</template>

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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
'''


    def _get_types(self) -> str:
        return '''/**
 * Type definitions for the frontend application.
 * Auto-generated types from backend will be in api.generated.ts
 */

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
    
    <div class="stats">
      <h3>System Status</h3>
      <p>Backend API: <span :class="apiStatus">{{ apiStatus }}</span></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '@/services/api'

const appName = import.meta.env.VITE_APP_NAME || 'Vue + FastAPI App'
const apiStatus = ref<'checking' | 'online' | 'offline'>('checking')

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