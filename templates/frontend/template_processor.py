"""
Template processor utility for frontend configuration templates.

This module provides utilities for loading and processing parameterized templates
for frontend configuration files across different frameworks.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class TemplateProcessor:
    """Process parameterized templates with framework-specific values."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize with templates directory path."""
        self.templates_dir = templates_dir or Path(__file__).parent
    
    def load_template(self, template_name: str) -> str:
        """Load a template file by name."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        return template_path.read_text(encoding='utf-8')
    
    def process_template(self, template_content: str, placeholders: Dict[str, str]) -> str:
        """Replace placeholders in template content."""
        result = template_content
        for key, value in placeholders.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, value)
        return result
    
    def generate_package_json(self, placeholders: Dict[str, str]) -> Dict[str, Any]:
        """Generate and parse package.json from template."""
        template = self.load_template("package.json.template")
        processed = self.process_template(template, placeholders)
        return json.loads(processed)
    
    def generate_config_file(self, template_name: str, placeholders: Dict[str, str]) -> str:
        """Generate any config file from template."""
        template = self.load_template(template_name)
        return self.process_template(template, placeholders)


# Example framework-specific placeholder configurations

REACT_PLACEHOLDERS = {
    "project_name": "my-react-app",
    "project_title": "My React App",
    "module_type": "module",
    "dev_command": "vite",
    "build_command": "tsc && vite build",
    "type_check_command": "tsc --noEmit",
    "lint_command": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "format_command": "prettier --write 'src/**/*.{ts,tsx,css}'",
    "test_command": "vitest",
    "framework_scripts": ',\n    "test:ui": "vitest --ui"',
    "framework_dependencies": ',\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0",\n    "react-router-dom": "^6.20.0",\n    "@tanstack/react-query": "^5.0.0",\n    "zustand": "^4.4.0"',
    "dev_dependencies": ',\n    "@types/react": "^18.2.0",\n    "@types/react-dom": "^18.2.0",\n    "@vitejs/plugin-react": "^4.2.0",\n    "eslint-plugin-react-hooks": "^4.6.0",\n    "eslint-plugin-react-refresh": "^0.4.0"',
    "framework_imports": "import react from '@vitejs/plugin-react'",
    "framework_plugins": "react()",
    "path_aliases": "",
    "build_options": "",
    "test_config": "",
    "include_paths": '"src"',
    "path_mappings": ',\n      "@/components/*": ["src/components/*"],\n      "@/hooks/*": ["src/hooks/*"]',
    "compiler_options": ',\n    "jsx": "react-jsx"',
    "references": ',\n  "references": [{"path": "./tsconfig.node.json"}]',
    "env_prefix": "VITE",
    "framework_specific_vars": "",
    "components_pattern": "src/components/*",
    "pages_type": "pages",
    "pages_pattern": "src/pages/*", 
    "state_type": "stores",
    "state_pattern": "src/stores/*",
    "component_hook_type": "hooks",
    "framework_eslint_extends": ',\n    "plugin:react-hooks/recommended"',
    "framework_eslint_plugins": "'react-refresh'",
    "restricted_import_message": "Components should use hooks or higher-level services for API calls",
    "framework_specific_rules": "    'react-refresh/only-export-components': [\n      'warn',\n      { allowConstantExport: true },\n    ],",
    "test_environment": "jsdom",
    "file_extensions": ",tsx",
    "setup_files": "'src/test-setup.ts'",
    "test_file_extensions": ",tsx",
    "test_options": ""
}

VUE_PLACEHOLDERS = {
    "project_name": "my-vue-app", 
    "project_title": "My Vue App",
    "module_type": "module",
    "dev_command": "vite",
    "build_command": "run-p type-check build-only", 
    "type_check_command": "vue-tsc --noEmit -p tsconfig.app.json --composite false",
    "lint_command": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore",
    "format_command": "prettier --write src/",
    "test_command": "vitest",
    "framework_scripts": ',\n    "build-only": "vite build",\n    "test:unit": "vitest --environment jsdom --root src/"',
    "framework_dependencies": ',\n    "vue": "^3.4.0",\n    "vue-router": "^4.2.5",\n    "pinia": "^2.1.7",\n    "@vueuse/core": "^10.7.0"',
    "dev_dependencies": ',\n    "@vitejs/plugin-vue": "^4.5.0",\n    "@vue/eslint-config-typescript": "^12.0.0",\n    "eslint-plugin-vue": "^9.17.0",\n    "vue-tsc": "^1.8.25"',
    "framework_imports": "import vue from '@vitejs/plugin-vue'",
    "framework_plugins": "vue()",
    "include_paths": '"src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"',
    "path_mappings": "",
    "compiler_options": ',\n    "jsx": "preserve"',
    "references": ',\n  "references": [\n    {"path": "./tsconfig.node.json"},\n    {"path": "./tsconfig.app.json"}\n  ]',
    "env_prefix": "VITE", 
    "framework_specific_vars": "",
    "components_pattern": "src/components/*",
    "pages_type": "views",
    "pages_pattern": "src/views/*",
    "state_type": "stores", 
    "state_pattern": "src/stores/*",
    "component_hook_type": "composables",
    "framework_eslint_extends": ',\n    "plugin:vue/vue3-essential",\n    "@vue/eslint-config-prettier/skip-formatting"',
    "framework_eslint_plugins": "",
    "restricted_import_message": "Components should use composables or higher-level services for API calls",
    "framework_specific_rules": "    'vue/multi-word-component-names': 'off',\n    'vue/no-unused-vars': 'error'",
    "test_environment": "jsdom",
    "file_extensions": ",vue",
    "setup_files": "'src/test-setup.ts'", 
    "test_file_extensions": ",vue",
    "test_options": ""
}

SVELTE_PLACEHOLDERS = {
    "project_name": "my-svelte-app",
    "project_title": "My Svelte App", 
    "module_type": "module",
    "dev_command": "vite dev",
    "build_command": "vite build",
    "type_check_command": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
    "lint_command": "eslint . --ext .svelte,.js,.ts --report-unused-disable-directives --max-warnings 0",
    "format_command": "prettier --write 'src/**/*.{svelte,js,ts,css,md}'",
    "test_command": "vitest",
    "framework_scripts": ',\n    "test:coverage": "vitest --coverage"',
    "framework_dependencies": ',\n    "svelte": "^5.0.0"',
    "dev_dependencies": ',\n    "@sveltejs/kit": "^2.0.0",\n    "@sveltejs/adapter-auto": "^3.0.0",\n    "@sveltejs/vite-plugin-svelte": "^4.0.0",\n    "svelte-check": "^4.0.0",\n    "eslint-plugin-svelte": "^2.35.0"',
    "framework_imports": "import { sveltekit } from '@sveltejs/kit/vite'",
    "framework_plugins": "sveltekit()",
    "include_paths": '".svelte-kit/tsconfig.json"',
    "compiler_options": "",
    "references": "",
    "env_prefix": "PUBLIC",
    "framework_specific_vars": '\n\n# Private environment variables (not exposed to client)\nPRIVATE_API_KEY=your-private-api-key-here',
    "components_pattern": "src/lib/components/*", 
    "pages_type": "routes",
    "pages_pattern": "src/routes/*",
    "state_type": "stores",
    "state_pattern": "src/lib/stores/*",
    "component_hook_type": "composables", 
    "framework_eslint_extends": ',\n    "plugin:svelte/recommended"',
    "framework_eslint_plugins": "'svelte'",
    "restricted_import_message": "Components should use composables or higher-level services for API calls",
    "framework_specific_rules": "    // Svelte-specific rules\n    'svelte/no-unused-svelte-ignore': 'error'",
    "test_environment": "jsdom",
    "file_extensions": ",svelte",
    "setup_files": "'src/lib/test-setup.ts'",
    "test_file_extensions": ",svelte", 
    "test_options": ""
}


# Example usage
if __name__ == "__main__":
    processor = TemplateProcessor()
    
    # Generate React package.json
    react_package = processor.generate_package_json(REACT_PLACEHOLDERS)
    print("React package.json generated:")
    print(json.dumps(react_package, indent=2))
    
    # Generate Vue vite config
    vue_vite_config = processor.generate_config_file("vite.config.ts.template", VUE_PLACEHOLDERS)
    print("\nVue vite.config.ts generated:")
    print(vue_vite_config)