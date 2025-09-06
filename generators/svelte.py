"""
Svelte 5 + SvelteKit frontend generator for monorepo bootstrap.
Implements modern Svelte 5 runes, TypeScript, and SvelteKit patterns.
"""

from pathlib import Path
from typing import Dict, Any, List

from .base_frontend import BaseFrontendGenerator
from .svelte_components import SvelteComponentsGenerator
from .svelte_stores_composables import SvelteStoresComposablesGenerator
from .svelte_forms import SvelteFormsGenerator
from .svelte_layouts import SvelteLayoutsGenerator
from .svelte_actions_utils import SvelteActionsUtilsGenerator
from .svelte_barrel_exports import SvelteBarrelExportsGenerator


class SvelteFrontendGenerator(BaseFrontendGenerator):
    
    def get_framework_name(self) -> str:
        """Return the name of the framework."""
        return "Svelte"
    
    def get_framework_directories(self) -> List[str]:
        """Return SvelteKit-specific directory paths to create."""
        return [
            "frontend/src/lib",
            "frontend/src/lib/components",
            "frontend/src/lib/components/ui",
            "frontend/src/lib/components/ui/Button",
            "frontend/src/lib/components/ui/Input", 
            "frontend/src/lib/components/ui/Modal",
            "frontend/src/lib/components/ui/Card",
            "frontend/src/lib/components/layout",
            "frontend/src/lib/components/layout/Header",
            "frontend/src/lib/components/layout/Sidebar", 
            "frontend/src/lib/components/layout/Footer",
            "frontend/src/lib/components/forms",
            "frontend/src/lib/components/forms/UserForm",
            "frontend/src/lib/components/forms/LoginForm",
            "frontend/src/lib/components/forms/ContactForm",
            "frontend/src/lib/components/features",
            "frontend/src/lib/components/features/auth",
            "frontend/src/lib/components/features/dashboard",
            "frontend/src/lib/components/features/profile",
            "frontend/src/lib/stores",
            "frontend/src/lib/composables",
            "frontend/src/lib/actions",
            "frontend/src/lib/utils",
            "frontend/src/lib/types",
            "frontend/src/lib/schemas",
            "frontend/src/lib/config",
            "frontend/src/routes",
            "frontend/src/routes/(app)",
            "frontend/src/routes/(app)/dashboard",
            "frontend/src/routes/(auth)",
            "frontend/src/routes/(auth)/login",
            "frontend/src/routes/(marketing)",
            "frontend/src/routes/about",
            "frontend/src/routes/contact",
            "frontend/src/routes/api",
            "frontend/src/params",
            "frontend/static",
            "frontend/static/images",
            "frontend/static/images/icons",
            "frontend/static/fonts"
        ]
    
    def get_framework_dependencies(self) -> Dict[str, str]:
        """Return Svelte-specific runtime dependencies."""
        return {
            "svelte": "^5.0.0",
            "zod": "^3.22.0"
        }
    
    def get_framework_dev_dependencies(self) -> Dict[str, str]:
        """Return Svelte-specific development dependencies."""
        return {
            "@sveltejs/kit": "^2.0.0",
            "@sveltejs/adapter-auto": "^3.0.0", 
            "@sveltejs/vite-plugin-svelte": "^4.0.0",
            "svelte-check": "^4.0.0"
        }
    
    def get_framework_test_dependencies(self) -> Dict[str, str]:
        """Return Svelte-specific test dependencies."""
        return {
            "@testing-library/svelte": "^5.0.0"
        }
    
    def get_framework_lint_dependencies(self) -> Dict[str, str]:
        """Return Svelte-specific linting dependencies."""
        return {
            "eslint-plugin-svelte": "^2.35.0",
            "prettier-plugin-svelte": "^3.0.0"
        }
    
    def get_framework_scripts(self) -> Dict[str, str]:
        """Return Svelte-specific npm scripts."""
        return {
            "dev": "vite dev",
            "build": "vite build",
            "preview": "vite preview",
            "type-check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
            "postinstall": "svelte-kit sync"
        }
    
    def get_vite_plugin_import(self) -> str:
        """Return the import statement for Svelte's Vite plugin."""
        return "import { sveltekit } from '@sveltejs/kit/vite'"
    
    def get_vite_plugin_usage(self) -> str:
        """Return the usage of Svelte's Vite plugin."""
        return "sveltekit()"
    
    def customize_tsconfig(self, config: Dict[str, Any]) -> None:
        """Customize TypeScript configuration for SvelteKit."""
        # SvelteKit uses its own tsconfig that extends generated config
        config.clear()
        config.update({
            "extends": "./.svelte-kit/tsconfig.json",
            "compilerOptions": {
                "allowJs": True,
                "checkJs": True,
                "esModuleInterop": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "skipLibCheck": True,
                "sourceMap": True,
                "strict": True
            }
        })
    
    def get_eslint_framework_extends(self) -> str:
        """Return Svelte-specific ESLint extends configuration."""
        return "\n    'plugin:svelte/recommended',"
    
    def get_eslint_framework_plugins(self) -> str:
        """Return Svelte-specific ESLint plugins."""
        return ", 'svelte'"
    
    def get_eslint_framework_rules(self) -> str:
        """Return Svelte-specific ESLint rules."""
        return '''\n    'svelte/no-at-html-tags': 'error',
    'svelte/no-target-blank': 'error','''
    
    def get_eslint_boundary_patterns(self) -> str:
        """Return Svelte-specific boundary patterns for ESLint."""
        return '''\n      {
        type: 'ui-components',
        pattern: 'src/lib/components/ui/*',
        mode: 'folder'
      },
      {
        type: 'layout-components',
        pattern: 'src/lib/components/layout/*',
        mode: 'folder'
      },
      {
        type: 'form-components',
        pattern: 'src/lib/components/forms/*',
        mode: 'folder'
      },
      {
        type: 'feature-components',
        pattern: 'src/lib/components/features/*',
        mode: 'folder'
      },
      {
        type: 'routes',
        pattern: 'src/routes/*',
        mode: 'folder'
      },
      {
        type: 'stores',
        pattern: 'src/lib/stores/*',
        mode: 'folder'
      },
      {
        type: 'composables',
        pattern: 'src/lib/composables/*',
        mode: 'folder'
      },
      {
        type: 'actions',
        pattern: 'src/lib/actions/*',
        mode: 'folder'
      },
      {
        type: 'utils',
        pattern: 'src/lib/utils/*',
        mode: 'folder'
      },
      {
        type: 'types',
        pattern: 'src/lib/types/*',
        mode: 'folder'
      },
      {
        type: 'schemas',
        pattern: 'src/lib/schemas/*',
        mode: 'folder'
      },
      {
        type: 'config',
        pattern: 'src/lib/config/*',
        mode: 'folder'
      }'''
    
    def get_lint_command(self) -> str:
        """Return the lint command for Svelte."""
        return "eslint . --ext .svelte,.js,.ts --report-unused-disable-directives --max-warnings 0"
    
    def get_lint_fix_command(self) -> str:
        """Return the lint fix command for Svelte.""" 
        return "eslint . --ext .svelte,.js,.ts --fix"
    
    def get_test_file_extensions(self) -> str:
        """Return Svelte-specific test file extensions."""
        return ",.svelte"
    
    def create_framework_configs(self) -> None:
        """Create SvelteKit-specific configuration files."""
        # Create svelte.config.js
        svelte_config = '''import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations#preprocessors
  // for more information about preprocessors
  preprocess: vitePreprocess(),

  kit: {
    // adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
    // If your environment is not supported or you settled on a specific environment, switch out the adapter.
    // See https://svelte.dev/docs/kit/adapters for more information about adapters.
    adapter: adapter(),

    // Configure alias paths
    alias: {
      $lib: 'src/lib',
      $components: 'src/lib/components',
      $stores: 'src/lib/stores',
      $utils: 'src/lib/utils',
      $types: 'src/lib/types',
      $actions: 'src/lib/actions',
      $composables: 'src/lib/composables',
      $schemas: 'src/lib/schemas',
      $config: 'src/lib/config'
    }
  },

  // Enable Svelte 5 runes mode
  compilerOptions: {
    runes: true
  }
};

export default config;
'''
        (self.frontend_dir / "svelte.config.js").write_text(svelte_config)
        
        # Create app.html
        project_title = self.project_name.replace('_', ' ').title()
        app_html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%sveltekit.assets%/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{project_title}</title>
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
'''
        (self.frontend_dir / "src" / "app.html").write_text(app_html)

    def create_framework_routes(self) -> None:
        """Create SvelteKit routing structure with example routes."""
        print("  🛣️ Creating SvelteKit routes...")
        
        # Root layout (+layout.svelte)
        root_layout = '''<script lang="ts">
  import { onMount } from 'svelte';
  import { Header, Footer } from '$components/layout';
  import '../app.css';
  
  let { children } = $props();
</script>

<div class="app">
  <Header title="''' + self.project_name.replace('_', ' ').title() + '''" />
  
  <main class="main-content">
    {@render children()}
  </main>
  
  <Footer />
</div>

<style>
  :global(html) {
    --primary-color: #ff3e00;
    --text-color: #333;
    --text-secondary: #666;
    --border-color: #e0e0e0;
    --background-color: #fff;
  }

  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .main-content {
    flex: 1;
    padding: 2rem 1rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }

  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    line-height: 1.5;
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "+layout.svelte").write_text(root_layout)
        
        # Home page (+page.svelte)
        home_page = '''<script lang="ts">
  import { Card, Button } from '$components/ui';
  
  const features = [
    {
      title: 'SvelteKit',
      description: 'Full-stack web framework with modern routing and server-side rendering.',
      icon: '🚀'
    },
    {
      title: 'TypeScript',
      description: 'Type-safe development with excellent IDE support and error catching.',
      icon: '📝'
    },
    {
      title: 'Svelte 5 Runes',
      description: 'New reactivity system with fine-grained reactive state management.',
      icon: '⚡'
    },
    {
      title: 'Component Library',
      description: 'Pre-built UI components with consistent design and accessibility.',
      icon: '🧱'
    }
  ];
</script>

<svelte:head>
  <title>Welcome to ''' + self.project_name.replace('_', ' ').title() + '''</title>
  <meta name="description" content="A modern SvelteKit application" />
</svelte:head>

<div class="home">
  <section class="hero">
    <h1 class="hero-title">Welcome to ''' + self.project_name.replace('_', ' ').title() + '''</h1>
    <p class="hero-description">
      A modern web application built with SvelteKit, TypeScript, and Svelte 5 runes.
      Get started by exploring the features below.
    </p>
    <div class="hero-actions">
      <Button>
        <a href="/dashboard">Get Started</a>
      </Button>
      <Button variant="outline">
        <a href="/about">Learn More</a>
      </Button>
    </div>
  </section>

  <section class="features">
    <h2 class="features-title">Features</h2>
    <div class="features-grid">
      {#each features as feature}
        <Card variant="elevated">
          {#snippet header()}
            <div class="feature-header">
              <span class="feature-icon">{feature.icon}</span>
              <h3 class="feature-title">{feature.title}</h3>
            </div>
          {/snippet}
          
          <p class="feature-description">{feature.description}</p>
        </Card>
      {/each}
    </div>
  </section>
</div>

<style>
  .home {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .hero {
    text-align: center;
    margin-bottom: 4rem;
  }

  .hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 1rem;
  }

  .hero-description {
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.6;
  }

  .hero-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-actions a {
    color: inherit;
    text-decoration: none;
  }

  .features {
    margin-top: 4rem;
  }

  .features-title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: var(--text-color);
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
  }

  .feature-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .feature-icon {
    font-size: 2rem;
  }

  .feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: var(--text-color);
  }

  .feature-description {
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0;
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 2rem;
    }

    .hero-description {
      font-size: 1rem;
    }

    .features-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "+page.svelte").write_text(home_page)
        
        # About page
        about_page = '''<script lang="ts">
  import { Card } from '$components/ui';
</script>

<svelte:head>
  <title>About - ''' + self.project_name.replace('_', ' ').title() + '''</title>
</svelte:head>

<div class="about">
  <h1>About ''' + self.project_name.replace('_', ' ').title() + '''</h1>
  
  <Card>
    <p>
      This application was built with modern web technologies to provide 
      a fast, reliable, and user-friendly experience.
    </p>
    
    <h2>Technology Stack</h2>
    <ul>
      <li><strong>SvelteKit</strong> - Full-stack web framework</li>
      <li><strong>TypeScript</strong> - Type-safe JavaScript</li>
      <li><strong>Svelte 5</strong> - Reactive UI framework with runes</li>
      <li><strong>Vite</strong> - Fast development and build tool</li>
    </ul>
  </Card>
</div>

<style>
  .about {
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    color: var(--text-color);
    margin-bottom: 2rem;
  }
  
  h2 {
    color: var(--text-color);
    margin-top: 2rem;
    margin-bottom: 1rem;
  }
  
  p {
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
  }
  
  ul {
    line-height: 1.6;
    color: var(--text-secondary);
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  
  strong {
    color: var(--text-color);
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "about" / "+page.svelte").write_text(about_page)
        
        # Contact page
        contact_page = '''<script lang="ts">
  import { ContactForm } from '$components/forms';
  
  async function handleContactSubmit(data: any) {
    console.log('Contact form submitted:', data);
    // Implement actual contact form submission logic
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
</script>

<svelte:head>
  <title>Contact - ''' + self.project_name.replace('_', ' ').title() + '''</title>
</svelte:head>

<div class="contact">
  <ContactForm onSubmit={handleContactSubmit} />
</div>

<style>
  .contact {
    max-width: 600px;
    margin: 0 auto;
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "contact" / "+page.svelte").write_text(contact_page)
        
        # App CSS
        app_css = '''/* Global styles */
:root {
  --primary-color: #ff3e00;
  --text-color: #333;
  --text-secondary: #666;
  --border-color: #e0e0e0;
  --background-color: #fff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  line-height: 1.5;
  color: var(--text-color);
  background-color: var(--background-color);
}

h1, h2, h3, h4, h5, h6 {
  margin: 0 0 1rem 0;
  font-weight: 600;
  line-height: 1.2;
}

p {
  margin: 0 0 1rem 0;
}

a {
  color: var(--primary-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  font-family: inherit;
}

/* Utility classes */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
'''
        (self.frontend_dir / "src" / "app.css").write_text(app_css)
        
        print("  ✓ SvelteKit routes created")

    def create_framework_components(self) -> None:
        """Create Svelte-specific starter components."""
        # Create barrel exports first
        barrel_exports_generator = SvelteBarrelExportsGenerator(self.frontend_dir, self.project_name)
        barrel_exports_generator.create_barrel_exports()
        
        # Create UI components using dedicated generator
        ui_components_generator = SvelteComponentsGenerator(self.frontend_dir, self.project_name)
        ui_components_generator.create_ui_components()
        
        # Create form components using dedicated generator
        forms_generator = SvelteFormsGenerator(self.frontend_dir, self.project_name)
        forms_generator.create_form_components()
        
        # Create layout components using dedicated generator
        layouts_generator = SvelteLayoutsGenerator(self.frontend_dir, self.project_name)
        layouts_generator.create_layout_components()
        
        # Create stores and composables using dedicated generator
        stores_composables_generator = SvelteStoresComposablesGenerator(self.frontend_dir, self.project_name)
        stores_composables_generator.create_stores_and_composables()
        
        # Create actions, utilities, types, schemas, config, and params using dedicated generator
        actions_utils_generator = SvelteActionsUtilsGenerator(self.frontend_dir, self.project_name)
        actions_utils_generator.create_actions_and_utils()
        





    def create_framework_tests(self) -> None:
        """Create Svelte-specific test examples."""
        # Create example test for Card component
        card_test = '''import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Card from './Card.svelte';

describe('Card Component', () => {
  it('renders basic card structure', () => {
    render(Card, {
      props: {
        title: 'Test Card',
        content: 'Test content'
      }
    });

    expect(screen.getByText('Test Card')).toBeInTheDocument();
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });

  it('applies variant classes correctly', () => {
    const { container } = render(Card, {
      props: {
        title: 'Test Card',
        variant: 'elevated'
      }
    });

    const cardElement = container.querySelector('.card');
    expect(cardElement).toHaveClass('card--elevated');
  });

  it('handles missing optional props gracefully', () => {
    render(Card, {
      props: {
        title: 'Just Title'
      }
    });

    expect(screen.getByText('Just Title')).toBeInTheDocument();
  });
});
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Card" / "Card.test.ts").write_text(card_test)