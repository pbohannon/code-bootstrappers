"""
Svelte Barrel Exports Generator
Handles creation of index files and barrel exports for clean imports across the Svelte application.
"""

from pathlib import Path
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name


class SvelteBarrelExportsGenerator(BaseSvelteGenerator):
    """Generator for Svelte barrel exports and index files"""
    
    def create_barrel_exports(self) -> None:
        """Create index.ts barrel export files for clean imports."""
        print("  📦 Creating Svelte barrel exports...")
        
        # Create all barrel export files
        self._create_main_lib_barrel()
        self._create_components_barrel()
        self._create_ui_components_barrel()
        self._create_layout_components_barrel()
        self._create_forms_components_barrel()
        self._create_features_components_barrel()
        self._create_stores_barrel()
        self._create_utils_barrel()
        self._create_types_barrel()
        self._create_actions_barrel()
        self._create_composables_barrel()
        self._create_schemas_barrel()
        self._create_config_barrel()
        
        print("  ✓ Svelte barrel exports created")
    
    def _create_main_lib_barrel(self) -> None:
        """Create main lib barrel export."""
        lib_index = '''// Main library exports - Import anything from here

// Component exports
export * from './components/index.js';

// Store exports
export * from './stores/index.js';

// Utility exports
export * from './utils/index.js';

// Action exports  
export * from './actions/index.js';

// Composable exports
export * from './composables/index.js';

// Config exports
export * from './config/index.js';

// Type exports with namespace to avoid collisions
export * as Types from './types/index.js';

// Schema exports with namespace to avoid collisions  
export * as Schemas from './schemas/index.js';
'''
        (self.frontend_dir / "src" / "lib" / "index.ts").write_text(lib_index)
    
    def _create_components_barrel(self) -> None:
        """Create components barrel export."""
        components_index = '''// Component exports organized by category
export * from './ui/index.js';
export * from './layout/index.js';
export * from './forms/index.js';
export * from './features/index.js';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "index.ts").write_text(components_index)
    
    def _create_ui_components_barrel(self) -> None:
        """Create UI components barrel export."""
        ui_index = '''// Basic UI primitive components
export { default as Button } from './Button/Button.svelte';
export { default as Input } from './Input/Input.svelte';
export { default as Modal } from './Modal/Modal.svelte';
export { default as Card } from './Card/Card.svelte';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "index.ts").write_text(ui_index)
    
    def _create_layout_components_barrel(self) -> None:
        """Create layout components barrel export."""
        layout_index = '''// Layout and structural components
export { default as Header } from './Header/Header.svelte';
export { default as Sidebar } from './Sidebar/Sidebar.svelte';
export { default as Footer } from './Footer/Footer.svelte';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "index.ts").write_text(layout_index)
    
    def _create_forms_components_barrel(self) -> None:
        """Create forms components barrel export."""
        forms_index = '''// Form-specific components
export { default as UserForm } from './UserForm/UserForm.svelte';
export { default as LoginForm } from './LoginForm/LoginForm.svelte';
export { default as ContactForm } from './ContactForm/ContactForm.svelte';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "index.ts").write_text(forms_index)
    
    def _create_features_components_barrel(self) -> None:
        """Create features components barrel export."""
        features_index = '''// Feature-specific components
export * from './auth/index.js';
export * from './dashboard/index.js';
export * from './profile/index.js';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "features" / "index.ts").write_text(features_index)
        
        # Create feature-specific barrel exports
        auth_index = '''// Authentication feature components
// Add auth-specific components here as they are created
'''
        (self.frontend_dir / "src" / "lib" / "components" / "features" / "auth" / "index.ts").write_text(auth_index)
        
        dashboard_index = '''// Dashboard feature components
// Add dashboard-specific components here as they are created
'''
        (self.frontend_dir / "src" / "lib" / "components" / "features" / "dashboard" / "index.ts").write_text(dashboard_index)
        
        profile_index = '''// Profile feature components
// Add profile-specific components here as they are created
'''
        (self.frontend_dir / "src" / "lib" / "components" / "features" / "profile" / "index.ts").write_text(profile_index)
    
    def _create_stores_barrel(self) -> None:
        """Create stores barrel export."""
        stores_index = '''// Global state stores
export { authStore } from './auth.js';
export { themeStore } from './theme.js';
export { notificationStore } from './notifications.js';
export { globalStore, notify } from './global.js';
'''
        (self.frontend_dir / "src" / "lib" / "stores" / "index.ts").write_text(stores_index)
    
    def _create_utils_barrel(self) -> None:
        """Create utils barrel export."""
        utils_index = '''// Utility functions
export * from './date.js';
export * from './format.js';
export * from './validation.js';
export * from './api.js';
export * from './constants.js';
'''
        (self.frontend_dir / "src" / "lib" / "utils" / "index.ts").write_text(utils_index)
    
    def _create_types_barrel(self) -> None:
        """Create types barrel export."""
        types_index = '''// TypeScript type definitions
export type * from './api.js';
export type * from './auth.js';
export type * from './ui.js';
export type * from './global.js';
'''
        (self.frontend_dir / "src" / "lib" / "types" / "index.ts").write_text(types_index)
    
    def _create_actions_barrel(self) -> None:
        """Create actions barrel export."""
        actions_index = '''// Svelte actions
export { clickOutside } from './clickOutside.js';
export { focus } from './focus.js';
export { tooltip } from './tooltip.js';
'''
        (self.frontend_dir / "src" / "lib" / "actions" / "index.ts").write_text(actions_index)
    
    def _create_composables_barrel(self) -> None:
        """Create composables barrel export."""
        composables_index = '''// Reusable logic with Svelte 5 runes
export { useAuth } from './useAuth.js';
export { useApi } from './useApi.js';
export { useLocalStorage } from './useLocalStorage.js';
export { useDebounce } from './useDebounce.js';
export { usePagination } from './usePagination.js';
export { useUserData } from './useUserData.svelte.js';
'''
        (self.frontend_dir / "src" / "lib" / "composables" / "index.ts").write_text(composables_index)
    
    def _create_schemas_barrel(self) -> None:
        """Create schemas barrel export."""
        schemas_index = '''// Validation schemas
export * from './user.js';
export * from './forms.js';
export * from './api.js';
'''
        (self.frontend_dir / "src" / "lib" / "schemas" / "index.ts").write_text(schemas_index)
    
    def _create_config_barrel(self) -> None:
        """Create config barrel export."""
        config_index = '''// Configuration settings
export * from './database.js';
export * from './api.js';
export * from './auth.js';
'''
        (self.frontend_dir / "src" / "lib" / "config" / "index.ts").write_text(config_index)