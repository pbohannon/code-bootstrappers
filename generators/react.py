"""React frontend generator for monorepo bootstrap."""

from pathlib import Path
from typing import Dict, Any, List

from .base_frontend import BaseFrontendGenerator


class ReactFrontendGenerator(BaseFrontendGenerator):
    # Implement abstract methods from BaseFrontendGenerator
    
    def get_framework_name(self) -> str:
        """Return the name of the framework."""
        return "React"
    
    def get_framework_directories(self) -> List[str]:
        """Return React-specific directory paths to create."""
        return [
            "frontend/src/components",
            "frontend/src/pages", 
            "frontend/src/hooks",
            "frontend/src/stores"
        ]
    
    def get_framework_dependencies(self) -> Dict[str, str]:
        """Return React-specific runtime dependencies."""
        return {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "@tanstack/react-query": "^5.0.0",
            "zustand": "^4.4.0",
            "react-hook-form": "^7.48.0"
        }
    
    def get_framework_dev_dependencies(self) -> Dict[str, str]:
        """Return React-specific development dependencies."""
        return {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "@vitejs/plugin-react": "^4.2.0"
        }
    
    def get_framework_test_dependencies(self) -> Dict[str, str]:
        """Return React-specific test dependencies."""
        return {
            "@testing-library/react": "^14.0.0"
        }
    
    def get_framework_lint_dependencies(self) -> Dict[str, str]:
        """Return React-specific linting dependencies."""
        return {
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.0"
        }
    
    def get_framework_scripts(self) -> Dict[str, str]:
        """Return React-specific npm scripts."""
        return {
            "build": "tsc && vite build",
            "type-check": "tsc --noEmit"
        }
    
    def get_vite_plugin_import(self) -> str:
        """Return the import statement for React's Vite plugin."""
        return "import react from '@vitejs/plugin-react'"
    
    def get_vite_plugin_usage(self) -> str:
        """Return the usage of React's Vite plugin."""
        return "react()"
    
    def customize_tsconfig(self, config: Dict[str, Any]) -> None:
        """Customize TypeScript configuration for React."""
        # Add React-specific compiler options
        config["compilerOptions"].update({
            "useDefineForClassFields": True,
            "jsx": "react-jsx"
        })
        
        # Add React-specific path mappings
        config["compilerOptions"]["paths"].update({
            "@/components/*": ["src/components/*"],
            "@/hooks/*": ["src/hooks/*"],
            "@/stores/*": ["src/stores/*"],
            "@/pages/*": ["src/pages/*"]
        })
        
        # Add references for node config
        config["references"] = [{"path": "./tsconfig.node.json"}]
    
    def get_eslint_framework_extends(self) -> str:
        """Return React-specific ESLint extends configuration."""
        return "\n    'plugin:react-hooks/recommended',"
    
    def get_eslint_framework_plugins(self) -> str:
        """Return React-specific ESLint plugins."""
        return ", 'react-refresh'"
    
    def get_eslint_framework_rules(self) -> str:
        """Return React-specific ESLint rules."""
        return '''\n    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],'''
    
    def get_eslint_boundary_patterns(self) -> str:
        """Return React-specific boundary patterns for ESLint."""
        return '''\n      {
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
      }'''
    
    def get_lint_command(self) -> str:
        """Return the lint command for React."""
        return "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
    
    def get_lint_fix_command(self) -> str:
        """Return the lint fix command for React."""
        return "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0 --fix"
    
    def get_test_file_extensions(self) -> str:
        """Return React-specific test file extensions."""
        return ",tsx"
    
    def create_framework_configs(self) -> None:
        """Create React-specific configuration files."""
        # Create tsconfig.node.json for Vite
        tsconfig_node = {
            "compilerOptions": {
                "composite": True,
                "skipLibCheck": True,
                "module": "ESNext",
                "moduleResolution": "bundler",
                "allowSyntheticDefaultImports": True
            },
            "include": ["vite.config.ts"]
        }
        
        import json
        (self.frontend_dir / "tsconfig.node.json").write_text(
            json.dumps(tsconfig_node, indent=2)
        )
    
    def create_framework_routes(self) -> None:
        """Create React-specific routing setup."""
        # Create main App component with React Router
        app_component = f'''import {{ QueryClient, QueryClientProvider }} from '@tanstack/react-query';
import {{ BrowserRouter, Routes, Route }} from 'react-router-dom';
import HomePage from './pages/HomePage';

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
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={{<HomePage />}} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}}

export default App;
'''
        (self.frontend_dir / "src" / "App.tsx").write_text(app_component)
        
        # Create main.tsx entry point
        main_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
'''
        (self.frontend_dir / "src" / "main.tsx").write_text(main_tsx)
        
        # Create basic CSS
        index_css = '''@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.react:hover {
  filter: drop-shadow(0 0 2em #61dafbaa);
}

@keyframes logo-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: no-preference) {
  a:nth-of-type(2) .logo {
    animation: logo-spin infinite 20s linear;
  }
}

.card {
  padding: 2em;
}

.read-the-docs {
  color: #888;
}
'''
        (self.frontend_dir / "src" / "index.css").write_text(index_css)
    
    def create_framework_components(self) -> None:
        """Create React-specific starter components."""
        # Create HomePage component
        home_page = f'''import React from 'react';

const HomePage: React.FC = () => {{
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-8">
        Welcome to {self.project_name.replace('_', ' ').title()}
      </h1>
      <div className="max-w-2xl mx-auto text-center">
        <p className="text-lg text-gray-600 mb-8">
          Your React frontend is connected to the FastAPI backend.
        </p>
        <div className="space-x-4">
          <a 
            href="/api/v1/docs" 
            target="_blank" 
            rel="noopener noreferrer"
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            API Docs
          </a>
        </div>
      </div>
    </div>
  );
}};

export default HomePage;
'''
        (self.frontend_dir / "src" / "pages" / "HomePage.tsx").write_text(home_page)
        
        
        # Create a basic layout component
        layout_component = '''import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">App</h1>
            </div>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
};

export default Layout;
'''
        (self.frontend_dir / "src" / "components" / "Layout.tsx").write_text(layout_component)
        
        # Create index.html
        index_html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{self.project_name.replace('_', ' ').title()}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
        (self.frontend_dir / "public" / "index.html").write_text(index_html)