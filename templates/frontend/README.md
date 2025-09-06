# Frontend Configuration Templates

This directory contains parameterized template files for generating frontend configurations across different frameworks (React, Vue, Svelte).

## Template Files

### Core Configuration Templates

- **package.json.template** - Base package.json with framework-agnostic dependencies and scripts
- **tsconfig.json.template** - TypeScript configuration with framework-specific overrides
- **vite.config.ts.template** - Vite configuration with plugin system placeholders
- **vitest.config.ts.template** - Unified testing configuration for all frameworks
- **.eslintrc.js.template** - ESLint configuration with architectural boundaries
- **.env.example.template** - Environment variables template
- **index.html.template** - HTML template with framework-specific sections
- **.gitignore.template** - Git ignore patterns for frontend projects

## Template Placeholder System

Templates use `{{placeholder}}` syntax for parameterization. Each framework generator provides specific values:

### Common Placeholders

- `{{project_name}}` - Project name
- `{{project_title}}` - Human-readable project title
- `{{env_prefix}}` - Environment variable prefix (VITE, PUBLIC, etc.)

### Framework-Specific Placeholders

#### React Placeholders
- `{{framework_dependencies}}` - React-specific dependencies (react, react-dom, etc.)
- `{{framework_plugins}}` - Vite plugins: `react()`
- `{{framework_eslint_extends}}` - React ESLint configurations
- `{{dev_command}}` - `vite`
- `{{build_command}}` - `tsc && vite build`

#### Vue Placeholders
- `{{framework_dependencies}}` - Vue-specific dependencies (vue, pinia, etc.)
- `{{framework_plugins}}` - Vite plugins: `vue()`
- `{{framework_eslint_extends}}` - Vue ESLint configurations
- `{{dev_command}}` - `vite`
- `{{build_command}}` - `run-p type-check build-only`

#### Svelte Placeholders
- `{{framework_dependencies}}` - Svelte-specific dependencies
- `{{framework_plugins}}` - Vite plugins: `sveltekit()`
- `{{framework_eslint_extends}}` - Svelte ESLint configurations
- `{{dev_command}}` - `vite dev`
- `{{build_command}}` - `vite build`

### ESLint Architecture Placeholders

- `{{components_pattern}}` - Path pattern for components
- `{{pages_type}}` - Type name for pages/views (pages, views)
- `{{pages_pattern}}` - Path pattern for pages/views
- `{{state_type}}` - State management type (stores, hooks)
- `{{state_pattern}}` - State management path pattern
- `{{component_hook_type}}` - Component helper type (hooks, composables)

## Usage in Generator Classes

Generators should:

1. Load template files from this directory
2. Replace placeholders with framework-specific values
3. Write the processed templates to the target project

Example structure in a generator:

```python
def _load_template(self, template_name: str) -> str:
    template_path = Path(__file__).parent.parent / "templates" / "frontend" / template_name
    return template_path.read_text()

def _process_template(self, template_content: str, placeholders: Dict[str, str]) -> str:
    for key, value in placeholders.items():
        template_content = template_content.replace(f"{{{{{key}}}}}", value)
    return template_content
```

## Benefits

- **DRY Principle**: Eliminates duplication across generators
- **Consistency**: Ensures consistent configuration patterns
- **Maintainability**: Single source of truth for common configurations  
- **Extensibility**: Easy to add new frameworks or modify existing ones
- **Architecture Enforcement**: Consistent ESLint rules across all frameworks