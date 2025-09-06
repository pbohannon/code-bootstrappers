"""
Svelte Form Components Generator
Handles creation of form-specific components like UserForm, LoginForm, ContactForm, etc.
"""

from pathlib import Path
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name


class SvelteFormsGenerator(BaseSvelteGenerator):
    """Generator for Svelte form components"""
    
    def create_form_components(self) -> None:
        """Create all form components."""
        print("  📝 Creating Svelte form components...")
        
        # Create individual form components
        self._create_user_form()
        self._create_login_form() 
        self._create_contact_form()
        
        print("  ✓ Svelte form components created")
    
    def _create_user_form(self) -> None:
        """Create UserForm component."""
        user_form_component = '''<script lang="ts">
  import { Button, Input } from '$components/ui';
  import { userSchema } from '$lib/schemas/user';
  import type { User, CreateUser } from '$lib/types/auth';
  import type { Snippet } from 'svelte';

  interface Props {
    user?: Partial<User>;
    onSubmit: (userData: CreateUser) => Promise<void>;
    submitText?: string;
    children?: Snippet;
  }

  let { user = {}, onSubmit, submitText = 'Save User', children }: Props = $props();

  let formData = $state({
    name: user.name || '',
    email: user.email || '',
    role: user.role || 'user'
  });
  
  let errors = $state<Record<string, string>>({});
  let isSubmitting = $state(false);

  async function handleSubmit(event: Event) {
    event.preventDefault();
    isSubmitting = true;
    errors = {};

    try {
      const validatedData = userSchema.parse(formData);
      await onSubmit(validatedData);
    } catch (error: any) {
      if (error.issues) {
        // Zod validation errors
        for (const issue of error.issues) {
          errors[issue.path[0]] = issue.message;
        }
      } else {
        errors.general = error.message || 'An unexpected error occurred';
      }
    } finally {
      isSubmitting = false;
    }
  }

  function handleInputChange(field: string, value: string) {
    formData[field as keyof typeof formData] = value;
    // Clear error when user starts typing
    if (errors[field]) {
      delete errors[field];
    }
  }
</script>

<form onsubmit={handleSubmit} class="user-form">
  <div class="form-grid">
    <Input
      id="name"
      name="name"
      label="Full Name"
      value={formData.name}
      error={errors.name}
      required
      onchange={(value) => handleInputChange('name', value)}
    />

    <Input
      id="email"
      name="email"
      type="email"
      label="Email Address"
      value={formData.email}
      error={errors.email}
      required
      onchange={(value) => handleInputChange('email', value)}
    />

    <div class="select-group">
      <label for="role" class="label">
        Role <span class="required">*</span>
      </label>
      <select
        id="role"
        name="role"
        bind:value={formData.role}
        class="select"
        class:error={errors.role}
      >
        <option value="user">User</option>
        <option value="moderator">Moderator</option>
        <option value="admin">Admin</option>
      </select>
      {#if errors.role}
        <span class="error-message">{errors.role}</span>
      {/if}
    </div>
  </div>

  {#if errors.general}
    <div class="error-alert">
      {errors.general}
    </div>
  {/if}

  <div class="form-actions">
    <Button type="submit" disabled={isSubmitting}>
      {isSubmitting ? 'Saving...' : submitText}
    </Button>
    
    {#if children}
      {@render children()}
    {/if}
  </div>
</form>

<style>
  .user-form {
    max-width: 500px;
    margin: 0 auto;
  }

  .form-grid {
    display: grid;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .select-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-color, #333);
  }

  .required {
    color: #ef4444;
  }

  .select {
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border-color, #d1d5db);
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background: white;
  }

  .select:focus {
    outline: none;
    border-color: var(--primary-color, #ff3e00);
    box-shadow: 0 0 0 3px rgba(255, 62, 0, 0.1);
  }

  .select.error {
    border-color: #ef4444;
  }

  .error-message {
    font-size: 0.875rem;
    color: #ef4444;
  }

  .error-alert {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
  }

  .form-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "UserForm" / "UserForm.svelte").write_text(user_form_component)
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "UserForm" / "index.ts").write_text("export { default } from './UserForm.svelte';")
    
    def _create_login_form(self) -> None:
        """Create LoginForm component."""
        login_form_component = '''<script lang="ts">
  import { Button, Input } from '$components/ui';
  import { loginSchema } from '$lib/schemas/forms';
  import type { LoginForm } from '$lib/schemas/forms';

  interface Props {
    onSubmit: (credentials: LoginForm) => Promise<void>;
    onForgotPassword?: () => void;
    loading?: boolean;
  }

  let { onSubmit, onForgotPassword, loading = false }: Props = $props();

  let formData = $state({
    email: '',
    password: '',
    rememberMe: false
  });
  
  let errors = $state<Record<string, string>>({});
  let isSubmitting = $state(false);

  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (loading || isSubmitting) return;
    
    isSubmitting = true;
    errors = {};

    try {
      const validatedData = loginSchema.parse(formData);
      await onSubmit(validatedData);
    } catch (error: any) {
      if (error.issues) {
        // Zod validation errors
        for (const issue of error.issues) {
          errors[issue.path[0]] = issue.message;
        }
      } else {
        errors.general = error.message || 'Login failed. Please try again.';
      }
    } finally {
      isSubmitting = false;
    }
  }

  function handleInputChange(field: string, value: string) {
    formData[field as keyof typeof formData] = value;
    // Clear error when user starts typing
    if (errors[field]) {
      delete errors[field];
    }
  }
</script>

<form onsubmit={handleSubmit} class="login-form">
  <div class="form-header">
    <h1 class="title">Welcome Back</h1>
    <p class="subtitle">Sign in to your account</p>
  </div>

  <div class="form-fields">
    <Input
      id="email"
      name="email"
      type="email"
      label="Email"
      value={formData.email}
      error={errors.email}
      required
      placeholder="Enter your email"
      onchange={(value) => handleInputChange('email', value)}
    />

    <Input
      id="password"
      name="password"
      type="password"
      label="Password"
      value={formData.password}
      error={errors.password}
      required
      placeholder="Enter your password"
      onchange={(value) => handleInputChange('password', value)}
    />

    <div class="checkbox-group">
      <label class="checkbox-label">
        <input
          type="checkbox"
          bind:checked={formData.rememberMe}
          class="checkbox"
        />
        <span class="checkbox-text">Remember me</span>
      </label>
      
      {#if onForgotPassword}
        <button type="button" class="forgot-link" onclick={onForgotPassword}>
          Forgot password?
        </button>
      {/if}
    </div>
  </div>

  {#if errors.general}
    <div class="error-alert">
      {errors.general}
    </div>
  {/if}

  <Button type="submit" disabled={loading || isSubmitting} variant="primary" size="lg">
    {#if loading || isSubmitting}
      <span class="loading-spinner"></span>
      Signing in...
    {:else}
      Sign in
    {/if}
  </Button>
</form>

<style>
  .login-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .form-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .title {
    font-size: 1.875rem;
    font-weight: 700;
    color: var(--text-color, #111827);
    margin: 0 0 0.5rem 0;
  }

  .subtitle {
    color: var(--text-secondary, #6b7280);
    margin: 0;
  }

  .form-fields {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .checkbox-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }

  .checkbox {
    width: 1rem;
    height: 1rem;
    border: 1px solid #d1d5db;
    border-radius: 3px;
    background: white;
  }

  .checkbox:checked {
    background: var(--primary-color, #ff3e00);
    border-color: var(--primary-color, #ff3e00);
  }

  .checkbox-text {
    font-size: 0.875rem;
    color: var(--text-color, #374151);
  }

  .forgot-link {
    background: none;
    border: none;
    color: var(--primary-color, #ff3e00);
    font-size: 0.875rem;
    cursor: pointer;
    text-decoration: none;
  }

  .forgot-link:hover {
    text-decoration: underline;
  }

  .error-alert {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    text-align: center;
  }

  .loading-spinner {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 0.5rem;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "LoginForm" / "LoginForm.svelte").write_text(login_form_component)
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "LoginForm" / "index.ts").write_text("export { default } from './LoginForm.svelte';")
    
    def _create_contact_form(self) -> None:
        """Create ContactForm component."""
        contact_form_component = '''<script lang="ts">
  import { Button, Input } from '$components/ui';
  import { contactSchema } from '$lib/schemas/forms';
  import type { ContactForm } from '$lib/types/forms';

  interface Props {
    onSubmit: (data: ContactForm) => Promise<void>;
    successMessage?: string;
  }

  let { onSubmit, successMessage }: Props = $props();

  let formData = $state({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  
  let errors = $state<Record<string, string>>({});
  let isSubmitting = $state(false);
  let showSuccess = $state(false);

  async function handleSubmit(event: Event) {
    event.preventDefault();
    isSubmitting = true;
    errors = {};
    showSuccess = false;

    try {
      const validatedData = contactSchema.parse(formData);
      await onSubmit(validatedData);
      
      // Reset form on success
      formData = {
        name: '',
        email: '',
        subject: '',
        message: ''
      };
      showSuccess = true;
      
      // Hide success message after 5 seconds
      setTimeout(() => {
        showSuccess = false;
      }, 5000);
      
    } catch (error: any) {
      if (error.issues) {
        // Zod validation errors
        for (const issue of error.issues) {
          errors[issue.path[0]] = issue.message;
        }
      } else {
        errors.general = error.message || 'Failed to send message. Please try again.';
      }
    } finally {
      isSubmitting = false;
    }
  }

  function handleInputChange(field: string, value: string) {
    formData[field as keyof typeof formData] = value;
    // Clear error when user starts typing
    if (errors[field]) {
      delete errors[field];
    }
  }
</script>

<form onsubmit={handleSubmit} class="contact-form">
  <div class="form-header">
    <h2 class="title">Contact Us</h2>
    <p class="subtitle">We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
  </div>

  {#if showSuccess}
    <div class="success-alert">
      {successMessage || "Thank you for your message! We'll get back to you soon."}
    </div>
  {/if}

  <div class="form-grid">
    <Input
      id="name"
      name="name"
      label="Name"
      value={formData.name}
      error={errors.name}
      required
      placeholder="Your full name"
      onchange={(value) => handleInputChange('name', value)}
    />

    <Input
      id="email"
      name="email"
      type="email"
      label="Email"
      value={formData.email}
      error={errors.email}
      required
      placeholder="your.email@example.com"
      onchange={(value) => handleInputChange('email', value)}
    />

    <Input
      id="subject"
      name="subject"
      label="Subject"
      value={formData.subject}
      error={errors.subject}
      required
      placeholder="What is this about?"
      onchange={(value) => handleInputChange('subject', value)}
    />

    <div class="textarea-group">
      <label for="message" class="label">
        Message <span class="required">*</span>
      </label>
      <textarea
        id="message"
        name="message"
        bind:value={formData.message}
        class="textarea"
        class:error={errors.message}
        rows="5"
        placeholder="Tell us more about your inquiry..."
        oninput={(e) => handleInputChange('message', e.currentTarget.value)}
      ></textarea>
      {#if errors.message}
        <span class="error-message">{errors.message}</span>
      {/if}
    </div>
  </div>

  {#if errors.general}
    <div class="error-alert">
      {errors.general}
    </div>
  {/if}

  <div class="form-actions">
    <Button type="submit" disabled={isSubmitting} variant="primary" size="lg">
      {isSubmitting ? 'Sending...' : 'Send Message'}
    </Button>
  </div>
</form>

<style>
  .contact-form {
    max-width: 600px;
    margin: 0 auto;
  }

  .form-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .title {
    font-size: 1.875rem;
    font-weight: 700;
    color: var(--text-color, #111827);
    margin: 0 0 0.5rem 0;
  }

  .subtitle {
    color: var(--text-secondary, #6b7280);
    margin: 0;
    line-height: 1.5;
  }

  .form-grid {
    display: grid;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .textarea-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-color, #333);
  }

  .required {
    color: #ef4444;
  }

  .textarea {
    padding: 0.75rem;
    border: 1px solid var(--border-color, #d1d5db);
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background: white;
    resize: vertical;
    min-height: 120px;
  }

  .textarea:focus {
    outline: none;
    border-color: var(--primary-color, #ff3e00);
    box-shadow: 0 0 0 3px rgba(255, 62, 0, 0.1);
  }

  .textarea.error {
    border-color: #ef4444;
  }

  .error-message {
    font-size: 0.875rem;
    color: #ef4444;
  }

  .success-alert {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
    text-align: center;
  }

  .error-alert {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
    text-align: center;
  }

  .form-actions {
    text-align: center;
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "ContactForm" / "ContactForm.svelte").write_text(contact_form_component)
        (self.frontend_dir / "src" / "lib" / "components" / "forms" / "ContactForm" / "index.ts").write_text("export { default } from './ContactForm.svelte';")