"""
React frontend generator using BaseFrontendGenerator.
This demonstrates the massive code reduction achieved by the base class.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from .base_frontend import BaseFrontendGenerator


class ReactFrontendGenerator(BaseFrontendGenerator):
    """React-specific frontend generator extending the base class."""
    
    def get_framework_name(self) -> str:
        return "React"
    
    def get_framework_directories(self) -> List[str]:
        return [
            "frontend/src/components",
            "frontend/src/pages", 
            "frontend/src/hooks",
            "frontend/src/stores",
        ]
    
    def get_framework_dependencies(self) -> Dict[str, str]:
        return {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "@tanstack/react-query": "^5.0.0",
            "zustand": "^4.4.0",
            "react-hook-form": "^7.48.0",
        }
    
    def get_framework_dev_dependencies(self) -> Dict[str, str]:
        return {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "@vitejs/plugin-react": "^4.2.0",
        }
    
    def get_framework_scripts(self) -> Dict[str, str]:
        return {
            "build": "tsc && vite build",
            "type-check": "tsc --noEmit"
        }
    
    def get_vite_plugin_import(self) -> str:
        return "import react from '@vitejs/plugin-react'"
    
    def get_vite_plugin_usage(self) -> str:
        return "react()"
    
    def customize_tsconfig(self, config: Dict[str, Any]) -> None:
        config["compilerOptions"]["jsx"] = "react-jsx"
        config["references"] = [{"path": "./tsconfig.node.json"}]
    
    def get_eslint_framework_extends(self) -> str:
        return '''
    'plugin:react-hooks/recommended','''
    
    def get_eslint_framework_plugins(self) -> str:
        return ", 'react-refresh'"
    
    def get_eslint_framework_rules(self) -> str:
        return '''
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],'''
    
    def get_eslint_boundary_patterns(self) -> str:
        return '''
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
      }'''
    
    def get_lint_command(self) -> str:
        return "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
    
    def get_lint_fix_command(self) -> str:
        return "eslint . --ext ts,tsx --fix"
    
    def get_framework_test_dependencies(self) -> Dict[str, str]:
        return {
            "@testing-library/react": "^14.0.0",
        }
    
    def get_framework_lint_dependencies(self) -> Dict[str, str]:
        return {
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.0",
        }
    
    def create_framework_routes(self) -> None:
        """Create React routing setup."""
        # App component with routing
        app_component = f'''import {{ QueryClient, QueryClientProvider }} from '@tanstack/react-query';
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

export default App;'''
        
        (self.frontend_dir / "src" / "App.tsx").write_text(app_component)
        
        # Main entry point
        main_tsx = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)'''
        
        (self.frontend_dir / "src" / "main.tsx").write_text(main_tsx)
        
        # Index HTML
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
</html>'''
        
        (self.frontend_dir / "index.html").write_text(index_html)
    
    def create_framework_components(self) -> None:
        """Create React starter components."""
        # Basic CSS
        index_css = '''body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}'''
        
        (self.frontend_dir / "src" / "index.css").write_text(index_css)
    
    def create_framework_configs(self) -> None:
        """Create React-specific configuration files."""
        # tsconfig.node.json for Node.js tooling
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
        
        (self.frontend_dir / "tsconfig.node.json").write_text(
            json.dumps(tsconfig_node, indent=2)
        )
    
    def create_framework_tests(self) -> None:
        """Create React test examples."""
        if not self.features.testing:
            return
            
        # Example component test
        app_test = '''import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders welcome message', () => {
    render(<App />);
    expect(screen.getByText(/welcome to/i)).toBeInTheDocument();
  });
});'''
        
        (self.frontend_dir / "src" / "App.test.tsx").write_text(app_test)