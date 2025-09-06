<script lang="ts">
  import { Button, Input, Card } from '$components/ui';
  import { loginSchema } from '$schemas/forms';
  import type { LoginForm } from '$schemas/forms';
  import type { ActionData, PageData } from './$types.js';

  interface Props {
    data: PageData;
    form?: ActionData;
  }

  let { data, form }: Props = $props();

  let formData = $state<LoginForm>({
    email: '',
    password: '',
    rememberMe: false
  });

  let errors = $state<Record<string, string>>({});
  let isSubmitting = $state(false);

  function validateForm(): boolean {
    const result = loginSchema.safeParse(formData);
    
    if (!result.success) {
      errors = {};
      result.error.errors.forEach((error) => {
        errors[error.path[0] as string] = error.message;
      });
      return false;
    }
    
    errors = {};
    return true;
  }

  function handleSubmit() {
    if (!validateForm()) return;
    
    isSubmitting = true;
    // Form submission is handled by SvelteKit form actions
  }

  function handleInputChange(field: keyof LoginForm, value: string | boolean) {
    formData[field] = value as never;
    // Clear error when user starts typing
    if (errors[field]) {
      delete errors[field];
      errors = { ...errors };
    }
  }
</script>

<svelte:head>
  <title>Login - {{APP_NAME}}</title>
  <meta name="description" content="Sign in to your account" />
</svelte:head>

<div class="login-page">
  <div class="login-container">
    <Card variant="elevated" class="login-card">
      {#snippet header()}
        <div class="login-header">
          <h1>Welcome back</h1>
          <p>Sign in to your account to continue</p>
        </div>
      {/snippet}

      <form method="POST" onsubmit={handleSubmit} class="login-form">
        {#if form?.error}
          <div class="error-banner">
            {form.error}
          </div>
        {/if}

        <Input
          type="email"
          name="email"
          label="Email address"
          placeholder="Enter your email"
          required
          value={formData.email}
          error={errors.email}
          onchange={(value) => handleInputChange('email', value)}
        />

        <Input
          type="password"
          name="password"
          label="Password"
          placeholder="Enter your password"
          required
          value={formData.password}
          error={errors.password}
          onchange={(value) => handleInputChange('password', value)}
        />

        <div class="form-row">
          <label class="checkbox-label">
            <input
              type="checkbox"
              name="rememberMe"
              bind:checked={formData.rememberMe}
            />
            Remember me
          </label>

          <a href="/forgot-password" class="forgot-link">
            Forgot password?
          </a>
        </div>

        <Button
          type="submit"
          variant="primary"
          size="lg"
          disabled={isSubmitting}
          class="login-button"
        >
          {isSubmitting ? 'Signing in...' : 'Sign in'}
        </Button>

        <div class="signup-link">
          Don't have an account? 
          <a href="/register">Sign up</a>
        </div>
      </form>
    </Card>
  </div>
</div>

<style>
  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
  }

  .login-container {
    width: 100%;
    max-width: 400px;
  }

  :global(.login-card) {
    width: 100%;
  }

  .login-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .login-header h1 {
    margin: 0 0 0.5rem;
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
  }

  .login-header p {
    margin: 0;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .error-banner {
    padding: 0.75rem;
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 6px;
    color: #dc2626;
    font-size: 0.875rem;
  }

  .form-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: #374151;
    cursor: pointer;
  }

  .checkbox-label input {
    margin: 0;
  }

  .forgot-link {
    color: var(--primary-color, #ff3e00);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .forgot-link:hover {
    text-decoration: underline;
  }

  :global(.login-button) {
    width: 100%;
  }

  .signup-link {
    text-align: center;
    font-size: 0.875rem;
    color: #6b7280;
  }

  .signup-link a {
    color: var(--primary-color, #ff3e00);
    text-decoration: none;
    font-weight: 500;
  }

  .signup-link a:hover {
    text-decoration: underline;
  }
</style>