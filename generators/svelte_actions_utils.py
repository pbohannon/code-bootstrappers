"""
Svelte Actions and Utilities Generator
Handles creation of Svelte actions, utility functions, types, schemas, config files, and parameter matchers.
"""

from pathlib import Path
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name


class SvelteActionsUtilsGenerator(BaseSvelteGenerator):
    """Generator for Svelte actions and utility functions"""
    
    def create_actions_and_utils(self) -> None:
        """Create all actions and utility files."""
        print("  🔧 Creating Svelte actions and utilities...")
        
        # Create actions
        self.create_actions()
        
        # Create types
        self.create_types()
        
        # Create schemas
        self.create_schemas()
        
        # Create config files
        self.create_config_files()
        
        # Create parameter matchers
        self.create_parameter_matchers()
        
        print("  ✓ Svelte actions and utilities created")
    
    def create_actions(self) -> None:
        """Create Svelte actions."""
        # Create Svelte actions
        click_outside_action = '''import type { Action } from 'svelte/action';

export const clickOutside: Action<HTMLElement, () => void> = (node, callback) => {
  const handleClick = (event: MouseEvent) => {
    if (!node.contains(event.target as Node)) {
      callback();
    }
  };

  document.addEventListener('click', handleClick, true);

  return {
    destroy() {
      document.removeEventListener('click', handleClick, true);
    }
  };
};
'''
        (self.frontend_dir / "src" / "lib" / "actions" / "clickOutside.ts").write_text(click_outside_action)
        
        focus_action = '''import type { Action } from 'svelte/action';

export const focus: Action<HTMLElement, boolean> = (node, enabled = true) => {
  const update = (enabled: boolean) => {
    if (enabled) {
      node.focus();
    }
  };

  update(enabled);

  return {
    update,
    destroy() {
      // Cleanup if needed
    }
  };
};
'''
        (self.frontend_dir / "src" / "lib" / "actions" / "focus.ts").write_text(focus_action)
        
        tooltip_action = '''import type { Action } from 'svelte/action';

interface TooltipOptions {
  content: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
}

export const tooltip: Action<HTMLElement, TooltipOptions> = (node, options) => {
  let tooltipElement: HTMLElement | null = null;
  let timeout: NodeJS.Timeout;

  const showTooltip = () => {
    if (!options.content) return;

    tooltipElement = document.createElement('div');
    tooltipElement.className = 'tooltip';
    tooltipElement.textContent = options.content;
    tooltipElement.style.cssText = `
      position: absolute;
      background: #333;
      color: white;
      padding: 0.5rem;
      border-radius: 4px;
      font-size: 0.875rem;
      pointer-events: none;
      z-index: 1000;
      white-space: nowrap;
    `;

    document.body.appendChild(tooltipElement);

    const rect = node.getBoundingClientRect();
    const tooltipRect = tooltipElement.getBoundingClientRect();
    const position = options.position || 'top';

    let top = 0;
    let left = 0;

    switch (position) {
      case 'top':
        top = rect.top - tooltipRect.height - 8;
        left = rect.left + (rect.width - tooltipRect.width) / 2;
        break;
      case 'bottom':
        top = rect.bottom + 8;
        left = rect.left + (rect.width - tooltipRect.width) / 2;
        break;
      case 'left':
        top = rect.top + (rect.height - tooltipRect.height) / 2;
        left = rect.left - tooltipRect.width - 8;
        break;
      case 'right':
        top = rect.top + (rect.height - tooltipRect.height) / 2;
        left = rect.right + 8;
        break;
    }

    tooltipElement.style.top = `${Math.max(0, top)}px`;
    tooltipElement.style.left = `${Math.max(0, left)}px`;
  };

  const hideTooltip = () => {
    if (tooltipElement) {
      document.body.removeChild(tooltipElement);
      tooltipElement = null;
    }
  };

  const handleMouseEnter = () => {
    timeout = setTimeout(showTooltip, options.delay || 300);
  };

  const handleMouseLeave = () => {
    clearTimeout(timeout);
    hideTooltip();
  };

  node.addEventListener('mouseenter', handleMouseEnter);
  node.addEventListener('mouseleave', handleMouseLeave);

  return {
    update(newOptions: TooltipOptions) {
      options = newOptions;
    },
    destroy() {
      clearTimeout(timeout);
      node.removeEventListener('mouseenter', handleMouseEnter);
      node.removeEventListener('mouseleave', handleMouseLeave);
      hideTooltip();
    }
  };
};
'''
        (self.frontend_dir / "src" / "lib" / "actions" / "tooltip.ts").write_text(tooltip_action)

    def create_types(self) -> None:
        """Create TypeScript type definitions."""
        # Create TypeScript types
        api_types = '''// API related types
export interface ApiResponse<T = unknown> {
  data: T;
  meta?: PaginationMeta;
  error?: ApiError;
  success: boolean;
  message?: string;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  field?: string;
}

export interface ApiRequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  body?: unknown;
  timeout?: number;
}
'''
        (self.frontend_dir / "src" / "lib" / "types" / "api.ts").write_text(api_types)
        
        
        ui_types = '''// UI component related types
export interface ComponentProps {
  class?: string;
  id?: string;
  'data-testid'?: string;
}

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface ButtonProps extends ComponentProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
}

export type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';

export interface InputProps extends ComponentProps {
  type?: InputType;
  value?: string;
  placeholder?: string;
  label?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  readonly?: boolean;
}

export interface ModalProps extends ComponentProps {
  open: boolean;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closable?: boolean;
  maskClosable?: boolean;
}

export interface CardProps extends ComponentProps {
  variant?: 'default' | 'outlined' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export interface Theme {
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    error: string;
    info: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  borderRadius: {
    sm: string;
    md: string;
    lg: string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
  };
}
'''
        (self.frontend_dir / "src" / "lib" / "types" / "ui.ts").write_text(ui_types)
        
        global_types = '''// Global application types
export interface AppConfig {
  apiUrl: string;
  appName: string;
  version: string;
  environment: 'development' | 'staging' | 'production';
  features: FeatureFlags;
}

export interface FeatureFlags {
  darkMode: boolean;
  analytics: boolean;
  newDashboard: boolean;
  betaFeatures: boolean;
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
  actions?: NotificationAction[];
  timestamp: Date;
}

export interface NotificationAction {
  label: string;
  action: () => void;
  type?: 'primary' | 'secondary';
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
  progress?: number;
}

export interface ErrorState {
  hasError: boolean;
  error?: Error | string;
  errorId?: string;
}

export interface GlobalState {
  user: User | null;
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: Notification[];
  loading: LoadingState;
  error: ErrorState;
  config: AppConfig;
}

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

export type Prettify<T> = {
  [K in keyof T]: T[K];
} & {};
'''
        (self.frontend_dir / "src" / "lib" / "types" / "global.ts").write_text(global_types)

    def create_schemas(self) -> None:
        """Create validation schemas."""
        # Create validation schemas
        user_schema = '''import { z } from 'zod';

// User validation schemas
export const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2, 'Name must be at least 2 characters').max(50, 'Name must be less than 50 characters'),
  email: z.string().email('Invalid email address'),
  avatar: z.string().url().optional(),
  role: z.enum(['admin', 'moderator', 'user', 'guest']),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime()
});

export const userProfileSchema = userSchema.extend({
  bio: z.string().max(500, 'Bio must be less than 500 characters').optional(),
  location: z.string().max(100, 'Location must be less than 100 characters').optional(),
  website: z.string().url('Invalid website URL').optional(),
  preferences: z.object({
    theme: z.enum(['light', 'dark']),
    language: z.string(),
    notifications: z.object({
      email: z.boolean(),
      push: z.boolean(),
      sms: z.boolean(),
      marketing: z.boolean()
    })
  })
});

export const createUserSchema = z.object({
  name: userSchema.shape.name,
  email: userSchema.shape.email,
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one lowercase letter, one uppercase letter, and one number'),
  role: userSchema.shape.role.default('user')
});

export const updateUserSchema = createUserSchema
  .omit({ password: true })
  .partial()
  .extend({
    id: userSchema.shape.id
  });

export const changePasswordSchema = z.object({
  currentPassword: z.string().min(1, 'Current password is required'),
  newPassword: createUserSchema.shape.password,
  confirmPassword: z.string()
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});

// Type exports
export type User = z.infer<typeof userSchema>;
export type UserProfile = z.infer<typeof userProfileSchema>;
export type CreateUser = z.infer<typeof createUserSchema>;
export type UpdateUser = z.infer<typeof updateUserSchema>;
export type ChangePassword = z.infer<typeof changePasswordSchema>;
'''
        (self.frontend_dir / "src" / "lib" / "schemas" / "user.ts").write_text(user_schema)
        
        forms_schema = '''import { z } from 'zod';

// Form validation schemas
export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
  rememberMe: z.boolean().default(false)
});

export const registerSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one lowercase letter, one uppercase letter, and one number'),
  confirmPassword: z.string(),
  terms: z.boolean().refine(val => val === true, 'You must accept the terms and conditions')
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});

export const forgotPasswordSchema = z.object({
  email: z.string().email('Invalid email address')
});

export const resetPasswordSchema = z.object({
  token: z.string().min(1, 'Reset token is required'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one lowercase letter, one uppercase letter, and one number'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});

export const contactSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be less than 100 characters'),
  email: z.string().email('Invalid email address'),
  subject: z.string()
    .min(5, 'Subject must be at least 5 characters')
    .max(200, 'Subject must be less than 200 characters'),
  message: z.string()
    .min(10, 'Message must be at least 10 characters')
    .max(1000, 'Message must be less than 1000 characters')
});

export const profileUpdateSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),
  bio: z.string()
    .max(500, 'Bio must be less than 500 characters')
    .optional(),
  location: z.string()
    .max(100, 'Location must be less than 100 characters')
    .optional(),
  website: z.string()
    .url('Invalid website URL')
    .optional()
    .or(z.literal(''))
});

export const searchSchema = z.object({
  query: z.string()
    .min(1, 'Search query is required')
    .max(100, 'Search query must be less than 100 characters'),
  filters: z.object({
    category: z.string().optional(),
    dateRange: z.object({
      from: z.date().optional(),
      to: z.date().optional()
    }).optional(),
    sortBy: z.enum(['relevance', 'date', 'name']).default('relevance'),
    sortOrder: z.enum(['asc', 'desc']).default('desc')
  }).optional()
});

// Type exports
export type LoginForm = z.infer<typeof loginSchema>;
export type RegisterForm = z.infer<typeof registerSchema>;
export type ForgotPasswordForm = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordForm = z.infer<typeof resetPasswordSchema>;
export type ContactForm = z.infer<typeof contactSchema>;
export type ProfileUpdateForm = z.infer<typeof profileUpdateSchema>;
export type SearchForm = z.infer<typeof searchSchema>;
'''
        (self.frontend_dir / "src" / "lib" / "schemas" / "forms.ts").write_text(forms_schema)
        
        api_schema = '''import { z } from 'zod';

// API validation schemas
export const paginationSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(10),
  sortBy: z.string().optional(),
  sortOrder: z.enum(['asc', 'desc']).default('asc')
});

export const apiResponseSchema = z.object({
  success: z.boolean(),
  data: z.unknown(),
  message: z.string().optional(),
  meta: z.object({
    page: z.number(),
    limit: z.number(),
    total: z.number(),
    totalPages: z.number(),
    hasNext: z.boolean(),
    hasPrev: z.boolean()
  }).optional(),
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.record(z.unknown()).optional(),
    field: z.string().optional()
  }).optional()
});

export const healthCheckSchema = z.object({
  status: z.enum(['healthy', 'degraded', 'unhealthy']),
  timestamp: z.string().datetime(),
  version: z.string(),
  uptime: z.number(),
  services: z.record(z.object({
    status: z.enum(['up', 'down', 'degraded']),
    responseTime: z.number().optional(),
    message: z.string().optional()
  }))
});

export const errorResponseSchema = z.object({
  success: z.literal(false),
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.record(z.unknown()).optional(),
    field: z.string().optional()
  }),
  meta: z.object({
    requestId: z.string(),
    timestamp: z.string().datetime()
  }).optional()
});

// File upload schema
export const fileUploadSchema = z.object({
  file: z.instanceof(File),
  maxSize: z.number().default(5 * 1024 * 1024), // 5MB
  allowedTypes: z.array(z.string()).default(['image/jpeg', 'image/png', 'image/webp']),
  folder: z.string().optional()
});

// Batch operations schema
export const batchOperationSchema = z.object({
  operation: z.enum(['create', 'update', 'delete']),
  items: z.array(z.unknown()).min(1).max(100),
  options: z.object({
    continueOnError: z.boolean().default(false),
    returnErrors: z.boolean().default(true)
  }).optional()
});

// Type exports
export type PaginationParams = z.infer<typeof paginationSchema>;
export type ApiResponse<T = unknown> = Omit<z.infer<typeof apiResponseSchema>, 'data'> & { data: T };
export type HealthCheck = z.infer<typeof healthCheckSchema>;
export type ErrorResponse = z.infer<typeof errorResponseSchema>;
export type FileUpload = z.infer<typeof fileUploadSchema>;
export type BatchOperation = z.infer<typeof batchOperationSchema>;
'''
        (self.frontend_dir / "src" / "lib" / "schemas" / "api.ts").write_text(api_schema)

    def create_config_files(self) -> None:
        """Create configuration files."""
        # Create configuration files
        api_config = '''// API configuration
export const API_CONFIG = {
  baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  retries: 3,
  retryDelay: 1000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
} as const;

export const API_ENDPOINTS = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    register: '/auth/register',
    refresh: '/auth/refresh',
    profile: '/auth/profile',
    forgotPassword: '/auth/forgot-password',
    resetPassword: '/auth/reset-password'
  },
  users: {
    list: '/users',
    create: '/users',
    get: (id: string) => `/users/${id}`,
    update: (id: string) => `/users/${id}`,
    delete: (id: string) => `/users/${id}`
  },
  health: '/health'
} as const;

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500
} as const;
'''
        (self.frontend_dir / "src" / "lib" / "config" / "api.ts").write_text(api_config)
        
        
        database_config = f'''// Database configuration
export const DATABASE_CONFIG = {{
  name: '{self.project_name}',
  version: 1,
  stores: {{
    users: 'id',
    sessions: 'id',
    preferences: 'userId',
    cache: 'key'
  }}
}} as const;

export const CACHE_KEYS = {{
  USER_PROFILE: 'user_profile',
  API_CACHE: 'api_cache',
  THEME_PREFERENCE: 'theme_preference',
  LANGUAGE_PREFERENCE: 'language_preference'
}} as const;

export const STORAGE_KEYS = {{
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  THEME: 'theme',
  SIDEBAR_STATE: 'sidebar_state'
}} as const;
'''
        (self.frontend_dir / "src" / "lib" / "config" / "database.ts").write_text(database_config)

    def create_parameter_matchers(self) -> None:
        """Create parameter matchers."""
        # Create parameter matchers
        uuid_param = '''import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(param);
};
'''
        (self.frontend_dir / "src" / "params" / "uuid.ts").write_text(uuid_param)
        
        slug_param = '''import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
  const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  return slugRegex.test(param);
};
'''
        (self.frontend_dir / "src" / "params" / "slug.ts").write_text(slug_param)