# SvelteKit Best Practices Directory Structure

## Complete Project Structure

```
my-sveltekit-app/
├── src/
│   ├── app.html                          # SvelteKit app template
│   ├── app.d.ts                          # Global type definitions
│   ├── hooks.client.ts                   # Client-side hooks
│   ├── hooks.server.ts                   # Server-side hooks
│   ├── service-worker.ts                 # Service worker (optional)
│   │
│   ├── lib/                              # Shared library code
│   │   ├── components/                   # Reusable UI components
│   │   │   ├── ui/                       # Basic UI primitives
│   │   │   │   ├── Button/
│   │   │   │   │   ├── Button.svelte
│   │   │   │   │   ├── Button.test.ts
│   │   │   │   │   └── index.ts          # Barrel export
│   │   │   │   ├── Input/
│   │   │   │   │   ├── Input.svelte
│   │   │   │   │   ├── Input.test.ts
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Modal/
│   │   │   │   ├── Card/
│   │   │   │   └── index.ts              # Barrel export for all UI
│   │   │   │
│   │   │   ├── layout/                   # Layout components
│   │   │   │   ├── Header/
│   │   │   │   ├── Sidebar/
│   │   │   │   ├── Footer/
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── forms/                    # Form-specific components
│   │   │   │   ├── UserForm/
│   │   │   │   ├── LoginForm/
│   │   │   │   ├── ContactForm/
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── features/                 # Feature-specific components
│   │   │   │   ├── auth/
│   │   │   │   │   ├── LoginModal.svelte
│   │   │   │   │   ├── UserProfile.svelte
│   │   │   │   │   └── index.ts
│   │   │   │   ├── dashboard/
│   │   │   │   ├── analytics/
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── index.ts                  # Master barrel export
│   │   │
│   │   ├── stores/                       # Global state management
│   │   │   ├── auth.ts                   # Authentication store
│   │   │   ├── theme.ts                  # Theme/UI preferences
│   │   │   ├── notifications.ts          # App notifications
│   │   │   ├── cache.ts                  # Client-side caching
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   ├── composables/                  # Reusable logic (Svelte 5 runes)
│   │   │   ├── useAuth.ts                # Authentication logic
│   │   │   ├── useApi.ts                 # API interaction patterns
│   │   │   ├── useLocalStorage.ts        # Local storage management
│   │   │   ├── useDebounce.ts            # Debouncing logic
│   │   │   ├── usePagination.ts          # Pagination logic
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   ├── actions/                      # Svelte actions
│   │   │   ├── clickOutside.ts           # Click outside detector
│   │   │   ├── focus.ts                  # Focus management
│   │   │   ├── tooltip.ts                # Tooltip functionality
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   ├── utils/                        # Pure utility functions
│   │   │   ├── date.ts                   # Date manipulation
│   │   │   ├── format.ts                 # Formatting functions
│   │   │   ├── validation.ts             # Validation helpers
│   │   │   ├── api.ts                    # API utilities
│   │   │   ├── constants.ts              # App constants
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   ├── types/                        # TypeScript type definitions
│   │   │   ├── api.ts                    # API response types
│   │   │   ├── auth.ts                   # Authentication types
│   │   │   ├── ui.ts                     # UI component types
│   │   │   ├── database.ts               # Database schema types
│   │   │   ├── global.ts                 # Global type definitions
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   ├── schemas/                      # Validation schemas (Zod, etc.)
│   │   │   ├── user.ts                   # User validation schemas
│   │   │   ├── forms.ts                  # Form validation schemas
│   │   │   ├── api.ts                    # API request/response schemas
│   │   │   └── index.ts                  # Barrel export
│   │   │
│   │   └── config/                       # Configuration
│   │       ├── database.ts               # Database configuration
│   │       ├── api.ts                    # API configuration
│   │       ├── auth.ts                   # Auth configuration
│   │       └── index.ts                  # Barrel export
│   │
│   ├── routes/                           # SvelteKit routes
│   │   ├── (app)/                        # Route group for authenticated app
│   │   │   ├── +layout.svelte            # App layout
│   │   │   ├── +layout.server.ts         # App layout server logic
│   │   │   ├── +layout.ts                # App layout universal logic
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── +page.svelte          # Dashboard page component
│   │   │   │   ├── +page.server.ts       # Server-side logic
│   │   │   │   ├── +page.ts              # Universal logic
│   │   │   │   └── components/           # Page-specific components
│   │   │   │       ├── StatsCard.svelte
│   │   │   │       ├── ChartWidget.svelte
│   │   │   │       └── RecentActivity.svelte
│   │   │   │
│   │   │   ├── users/
│   │   │   │   ├── +page.svelte          # Users list page
│   │   │   │   ├── +page.server.ts
│   │   │   │   ├── components/
│   │   │   │   │   ├── UserTable.svelte
│   │   │   │   │   ├── UserFilters.svelte
│   │   │   │   │   └── UserActions.svelte
│   │   │   │   │
│   │   │   │   └── [id]/                 # Dynamic user routes
│   │   │   │       ├── +page.svelte      # User detail page
│   │   │   │       ├── +page.server.ts
│   │   │   │       ├── edit/
│   │   │   │       │   ├── +page.svelte
│   │   │   │       │   └── +page.server.ts
│   │   │   │       └── components/
│   │   │   │           ├── UserProfile.svelte
│   │   │   │           └── UserEditForm.svelte
│   │   │   │
│   │   │   └── settings/
│   │   │       ├── +page.svelte
│   │   │       ├── +page.server.ts
│   │   │       └── components/
│   │   │           ├── AccountSettings.svelte
│   │   │           ├── SecuritySettings.svelte
│   │   │           └── NotificationSettings.svelte
│   │   │
│   │   ├── (auth)/                       # Route group for authentication
│   │   │   ├── +layout.svelte            # Auth layout (minimal)
│   │   │   ├── login/
│   │   │   │   ├── +page.svelte
│   │   │   │   └── +page.server.ts
│   │   │   ├── register/
│   │   │   │   ├── +page.svelte
│   │   │   │   └── +page.server.ts
│   │   │   └── forgot-password/
│   │   │       ├── +page.svelte
│   │   │       └── +page.server.ts
│   │   │
│   │   ├── (marketing)/                  # Route group for public pages
│   │   │   ├── +layout.svelte            # Marketing layout
│   │   │   ├── +page.svelte              # Homepage
│   │   │   ├── about/
│   │   │   │   └── +page.svelte
│   │   │   ├── pricing/
│   │   │   │   └── +page.svelte
│   │   │   └── contact/
│   │   │       ├── +page.svelte
│   │   │       └── +page.server.ts
│   │   │
│   │   ├── api/                          # API routes
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   └── +server.ts
│   │   │   │   ├── logout/
│   │   │   │   │   └── +server.ts
│   │   │   │   └── refresh/
│   │   │   │       └── +server.ts
│   │   │   │
│   │   │   ├── users/
│   │   │   │   ├── +server.ts            # CRUD operations
│   │   │   │   └── [id]/
│   │   │   │       └── +server.ts
│   │   │   │
│   │   │   └── health/
│   │   │       └── +server.ts            # Health check endpoint
│   │   │
│   │   ├── +layout.svelte                # Root layout
│   │   ├── +layout.server.ts             # Root layout server logic
│   │   ├── +layout.ts                    # Root layout universal logic
│   │   ├── +error.svelte                 # Error page
│   │   └── +not-found.svelte             # 404 page
│   │
│   └── params/                           # Custom parameter matchers
│       ├── uuid.ts                       # UUID parameter matcher
│       └── slug.ts                       # Slug parameter matcher
│
├── static/                               # Static assets
│   ├── images/
│   │   ├── icons/                        # SVG icons
│   │   ├── logos/                        # Brand assets
│   │   └── avatars/                      # User avatars
│   ├── fonts/                            # Custom fonts
│   ├── favicon.ico                       # Favicon
│   └── manifest.json                     # PWA manifest
│
├── tests/                                # Test files
│   ├── unit/                             # Unit tests
│   │   ├── components/
│   │   ├── utils/
│   │   └── stores/
│   ├── integration/                      # Integration tests
│   ├── e2e/                              # End-to-end tests (Playwright)
│   └── fixtures/                         # Test data fixtures
│
├── docs/                                 # Documentation
│   ├── README.md                         # Project overview
│   ├── CONTRIBUTING.md                   # Contribution guidelines
│   ├── api/                              # API documentation
│   └── components/                       # Component documentation
│
├── scripts/                              # Build/deployment scripts
│   ├── build.js                          # Custom build script
│   ├── migrate.js                        # Database migration script
│   └── seed.js                           # Database seeding script
│
├── .env.example                          # Environment variables template
├── .env.local                            # Local environment (gitignored)
├── .gitignore                            # Git ignore rules
├── .eslintrc.cjs                         # ESLint configuration
├── .prettierrc                           # Prettier configuration
├── tsconfig.json                         # TypeScript configuration
├── vite.config.ts                        # Vite configuration
├── svelte.config.js                      # Svelte configuration
├── tailwind.config.js                    # Tailwind CSS configuration
├── playwright.config.ts                  # Playwright configuration
├── package.json                          # Package configuration
└── README.md                             # Project documentation
```

## Key Organizational Principles

### 1. Barrel Exports Pattern
Every directory with multiple files should have an `index.ts` that re-exports everything:

```ts
// lib/components/ui/index.ts
export { default as Button } from './Button/Button.svelte';
export { default as Input } from './Input/Input.svelte';
export { default as Modal } from './Modal/Modal.svelte';
export { default as Card } from './Card/Card.svelte';

// lib/composables/index.ts
export { useAuth } from './useAuth.js';
export { useApi } from './useApi.js';
export { useLocalStorage } from './useLocalStorage.js';
export { useDebounce } from './useDebounce.js';

// lib/index.ts (Master export)
export * from './components/index.js';
export * from './stores/index.js';
export * from './utils/index.js';
export * from './types/index.js';
```

### 2. Import Aliases Configuration
```ts
// vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  resolve: {
    alias: {
      $components: './src/lib/components',
      $stores: './src/lib/stores',
      $utils: './src/lib/utils',
      $types: './src/lib/types',
      $actions: './src/lib/actions',
      $composables: './src/lib/composables'
    }
  }
});
```

### 3. Clean Import Examples
```svelte
<script lang="ts">
  // ✅ Clean, predictable imports
  import { Button, Input, Modal } from '$components/ui';
  import { UserProfile, LoginForm } from '$components/features/auth';
  import { useAuth, useApi } from '$composables';
  import { authStore, themeStore } from '$stores';
  import { formatDate, validateEmail } from '$utils';
  import type { User, ApiResponse } from '$types';
</script>
```

### 4. Component Organization Rules

#### Small Components (< 50 lines)
```
Button/
├── Button.svelte       # Component implementation
├── Button.test.ts      # Unit tests
└── index.ts           # Export
```

#### Complex Components (> 50 lines)
```
UserDashboard/
├── UserDashboard.svelte        # Main component
├── UserDashboard.test.ts       # Tests
├── components/                 # Sub-components
│   ├── StatsSection.svelte
│   ├── ActivityFeed.svelte
│   └── QuickActions.svelte
├── stores/                     # Component-specific stores
│   └── userDashboard.ts
├── types.ts                    # Local types
└── index.ts                    # Export
```

### 5. Route-Specific Components
```
routes/users/[id]/
├── +page.svelte                # Page component (< 100 lines)
├── +page.server.ts             # Server logic
├── +page.ts                    # Universal logic
└── components/                 # Page-specific components only
    ├── UserProfile.svelte
    ├── UserStats.svelte
    └── UserActions.svelte
```

**Rule**: Page components should primarily orchestrate smaller components, not contain complex logic.

### 6. Store Organization Patterns
```ts
// stores/auth.ts - Domain-specific store
import { writable } from 'svelte/store';
import type { User } from '$types';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    loading: false,
    error: null
  });

  return {
    subscribe,
    login: async (credentials: LoginCredentials) => { /* ... */ },
    logout: () => { /* ... */ },
    refresh: async () => { /* ... */ },
    clearError: () => update(state => ({ ...state, error: null }))
  };
}

export const authStore = createAuthStore();
```

### 7. TypeScript Organization
```ts
// types/index.ts - Centralized type exports
export type { User, UserProfile, UserSettings } from './auth.js';
export type { ApiResponse, ApiError, PaginationMeta } from './api.js';
export type { ComponentProps, IconProps, ButtonVariant } from './ui.js';

// types/api.ts - API-specific types
export interface ApiResponse<T = unknown> {
  data: T;
  meta?: PaginationMeta;
  error?: ApiError;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  hasNext: boolean;
}
```

### 8. Validation Schema Organization
```ts
// schemas/user.ts
import { z } from 'zod';

export const userSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(18).max(120)
});

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

export type User = z.infer<typeof userSchema>;
export type LoginData = z.infer<typeof loginSchema>;
```

## Enforcement Tools

### 1. ESLint Configuration
```js
// .eslintrc.cjs
module.exports = {
  extends: [
    '@sveltejs/eslint-config-svelte',
    '@typescript-eslint/recommended'
  ],
  rules: {
    // Enforce barrel exports
    'no-restricted-imports': [
      'error',
      {
        patterns: [
          {
            group: ['../**/components/*/*'],
            message: 'Use barrel exports from $components instead'
          }
        ]
      }
    ],
    
    // Prevent massive components
    'max-lines': ['error', { max: 200, skipBlankLines: true }],
    
    // Require explicit return types
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};
```

### 2. Path Mapping in tsconfig.json
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "$lib": ["./src/lib"],
      "$lib/*": ["./src/lib/*"],
      "$components": ["./src/lib/components"],
      "$components/*": ["./src/lib/components/*"],
      "$stores": ["./src/lib/stores"],
      "$stores/*": ["./src/lib/stores/*"],
      "$utils": ["./src/lib/utils"],
      "$utils/*": ["./src/lib/utils/*"],
      "$types": ["./src/lib/types"],
      "$types/*": ["./src/lib/types/*"]
    }
  }
}
```

### 3. Conventional Commits
```bash
# Enforce conventional commits for better organization
feat(auth): add user login composable
fix(ui): resolve button focus issue  
refactor(store): migrate to Svelte 5 runes
docs(components): add Button component examples
```

## Benefits of This Structure

1. **Prevents Antipatterns**: Large components are naturally broken down
2. **Enforces Separation**: Clear boundaries between UI, logic, and data
3. **Scalable**: Works for small projects, grows with large teams
4. **Discoverable**: Predictable import paths and file locations
5. **Testable**: Co-located tests and clear dependencies
6. **Type-Safe**: Centralized type management
7. **SvelteKit Optimized**: Leverages framework conventions
8. **Team-Friendly**: Clear ownership and contribution patterns

This structure acts like "guardrails" - it makes the right thing easy and the wrong thing hard!