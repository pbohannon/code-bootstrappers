"""
Example of how frontend generators would use the template system.

This demonstrates the refactored approach where generators load templates
instead of hardcoding configurations as Python strings.
"""

import json
from pathlib import Path
from typing import Dict, Any
from template_processor import TemplateProcessor, REACT_PLACEHOLDERS


class RefactoredReactGenerator:
    """Example of how ReactFrontendGenerator would look after refactoring."""
    
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features
        self.templates_dir = Path(__file__).parent
        self.processor = TemplateProcessor(self.templates_dir)
    
    def create_structure(self):
        """Create React frontend structure using templates."""
        print("  🎨 Creating React frontend structure...")
        
        # Get React-specific placeholders
        placeholders = self._get_react_placeholders()
        
        # Generate configurations from templates
        self._generate_package_json(placeholders)
        self._generate_tsconfig(placeholders) 
        self._generate_vite_config(placeholders)
        self._generate_eslint_config(placeholders)
        self._generate_env_example(placeholders)
        
        # Generate other files that might still be custom per framework
        self._generate_custom_files()
        
        print("  ✓ React frontend structure created with templates")
    
    def _get_react_placeholders(self) -> Dict[str, str]:
        """Get React-specific template placeholders."""
        # Base placeholders from the example
        placeholders = REACT_PLACEHOLDERS.copy()
        
        # Override with actual project values
        placeholders.update({
            "project_name": self.project_name,
            "project_title": self.project_name.replace('_', ' ').title(),
        })
        
        # Add feature-specific dependencies/scripts
        if self.features.testing:
            placeholders["test_options"] = ',\n    coverage: {\n      reporter: ["text", "json", "html"]\n    }'
            placeholders["framework_scripts"] += ',\n    "test:coverage": "vitest --coverage"'
        
        return placeholders
    
    def _generate_package_json(self, placeholders: Dict[str, str]):
        """Generate package.json from template."""
        package_json = self.processor.generate_package_json(placeholders)
        
        target_path = self.project_dir / "frontend" / "package.json"
        target_path.write_text(json.dumps(package_json, indent=2))
    
    def _generate_tsconfig(self, placeholders: Dict[str, str]):
        """Generate tsconfig.json from template."""
        config_content = self.processor.generate_config_file("tsconfig.json.template", placeholders)
        
        target_path = self.project_dir / "frontend" / "tsconfig.json"
        target_path.write_text(config_content)
    
    def _generate_vite_config(self, placeholders: Dict[str, str]):
        """Generate vite.config.ts from template."""
        config_content = self.processor.generate_config_file("vite.config.ts.template", placeholders)
        
        target_path = self.project_dir / "frontend" / "vite.config.ts"
        target_path.write_text(config_content)
    
    def _generate_eslint_config(self, placeholders: Dict[str, str]):
        """Generate .eslintrc.js from template.""" 
        config_content = self.processor.generate_config_file(".eslintrc.js.template", placeholders)
        
        target_path = self.project_dir / "frontend" / ".eslintrc.js"
        target_path.write_text(config_content)
    
    def _generate_env_example(self, placeholders: Dict[str, str]):
        """Generate .env.example from template."""
        config_content = self.processor.generate_config_file(".env.example.template", placeholders)
        
        target_path = self.project_dir / "frontend" / ".env.example" 
        target_path.write_text(config_content)
    
    def _generate_custom_files(self):
        """Generate framework-specific files that don't use templates."""
        # These would still be custom per framework for now
        # Could be templated later if patterns emerge
        
        # API service (could be templated with different imports)
        api_service = self._get_api_service()
        (self.project_dir / "frontend" / "src" / "services" / "api.ts").write_text(api_service)
        
        # App component (framework-specific JSX/template syntax)
        app_component = self._get_app_component()
        (self.project_dir / "frontend" / "src" / "App.tsx").write_text(app_component)
    
    def _get_api_service(self) -> str:
        """Generate API service (could be templated later)."""
        # This could potentially be templated with different imports
        # based on framework (React Query vs Pinia vs Svelte stores)
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
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }
}

export const apiService = new ApiService();'''
    
    def _get_app_component(self) -> str:
        """Generate App component (framework-specific)."""
        return f'''import {{ QueryClient, QueryClientProvider }} from '@tanstack/react-query';
import {{ BrowserRouter }} from 'react-router-dom';

const queryClient = new QueryClient();

function App() {{
  return (
    <QueryClientProvider client={{queryClient}}>
      <BrowserRouter>
        <div className="App">
          <h1>Welcome to {self.project_name}</h1>
          <p>React frontend with template-generated configuration</p>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}}

export default App;'''


# Benefits of this approach:

"""
BEFORE (Hardcoded):
- Each generator had duplicate _get_package_json(), _get_tsconfig(), etc.
- 300+ lines of hardcoded JSON/config strings per generator
- Inconsistencies between frameworks
- Hard to maintain and update dependencies

AFTER (Template-based):
- Single source of truth for each config type
- ~50 lines per generator for config generation
- Consistent patterns across frameworks  
- Easy to update dependencies globally
- Clear separation of what's common vs framework-specific

Template System Benefits:
1. DRY Principle - No duplication of package.json, tsconfig, etc.
2. Consistency - All frameworks get same ESLint rules, prettier config
3. Maintainability - Update one template, affects all frameworks
4. Extensibility - Easy to add new frameworks or config files
5. Clarity - Obvious what's framework-specific vs common
"""