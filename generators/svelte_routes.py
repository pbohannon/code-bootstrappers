"""
Svelte 5 + SvelteKit routes generator for monorepo bootstrap.
Handles all route creation and page generation functionality.
"""

from pathlib import Path
from typing import Dict, Any, List

from .base_frontend import BaseFrontendGenerator


class SvelteRoutesGenerator(BaseFrontendGenerator):
    """
    Generator specifically for creating SvelteKit routes and pages.
    Extends BaseFrontendGenerator to handle all route-related functionality.
    """
    
    def get_framework_name(self) -> str:
        """Return the name of the framework."""
        return "Svelte"
    
    def create_framework_routes(self) -> None:
        """Create SvelteKit-specific routing setup."""
        # Create main app.svelte
        app_svelte = '''<script lang="ts">
  import './app.css';
</script>

<main>
  <slot />
</main>

<style>
  main {
    margin: 0 auto;
    max-width: 1200px;
    padding: 1rem;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: #fafafa;
    color: #333;
  }

  :global(*) {
    box-sizing: border-box;
  }
</style>
'''
        (self.frontend_dir / "src" / "app.svelte").write_text(app_svelte)
        
        # Create main page (+page.svelte) using external template
        main_page = self.load_and_substitute_template("pages/main_page.svelte")
        # Move main page to marketing route group
        (self.frontend_dir / "src" / "routes" / "(marketing)" / "+page.svelte").write_text(main_page)
        
        # Create page load function (+page.ts)
        main_page_load = '''import type { PageLoad } from './$types.js';

export const load: PageLoad = async ({ fetch, url }) => {
  // Example data loading
  const apiUrl = url.origin.replace('3000', '8000') + '/api/v1';

  try {
    // Optional: Fetch initial data from your FastAPI backend
    // const response = await fetch(`${apiUrl}/health`);
    // const healthData = await response.json();

    return {
      userId: 'demo-user',
      apiUrl,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.warn('Failed to load initial data:', error);

    return {
      userId: 'demo-user',
      apiUrl,
      timestamp: new Date().toISOString(),
      error: 'Failed to connect to API'
    };
  }
};
'''
        (self.frontend_dir / "src" / "routes" / "(marketing)" / "+page.ts").write_text(main_page_load)
        
        # Create marketing layout using external template
        marketing_layout = self.load_and_substitute_template("layouts/marketing_layout.svelte")
        (self.frontend_dir / "src" / "routes" / "(marketing)" / "+layout.svelte").write_text(marketing_layout)
        
        # Create auth routes using external template
        login_page = self.load_and_substitute_template("pages/login_page.svelte")
        (self.frontend_dir / "src" / "routes" / "(auth)" / "login" / "+page.svelte").write_text(login_page)
        
        # Create auth layout (minimal)
        auth_layout = '''<script lang="ts">
  import type { LayoutData } from './$types.js';
  import type { Snippet } from 'svelte';

  interface Props {
    data: LayoutData;
    children: Snippet;
  }

  let { data, children }: Props = $props();
</script>

<div class="auth-layout">
  {@render children()}
</div>

<style>
  .auth-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "(auth)" / "+layout.svelte").write_text(auth_layout)
        
        # Create app routes with dashboard
        dashboard_page = '''<script lang="ts">
  import { Card, Button } from '$components/ui';
  import { useUserData } from '$composables';
  import { globalStore, notify } from '$stores';
  import type { PageData } from './$types.js';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let { user, loading } = useUserData(data.userId);

  function handleNotificationTest() {
    notify.success('Dashboard loaded successfully!');
  }

  function handleThemeToggle() {
    globalStore.toggleTheme();
  }
</script>

<svelte:head>
  <title>Dashboard - SvelteKit App</title>
  <meta name="description" content="Your application dashboard" />
</svelte:head>

<div class="dashboard">
  <div class="dashboard-header">
    <h1>Dashboard</h1>
    <p class="subtitle">Welcome back{user ? `, ${user.name}` : ''}!</p>
  </div>

  <div class="dashboard-grid">
    <Card variant="elevated">
      {#snippet header()}
        <h3>📊 Statistics</h3>
      {/snippet}

      <div class="stats">
        <div class="stat">
          <div class="stat-value">1,234</div>
          <div class="stat-label">Total Users</div>
        </div>
        <div class="stat">
          <div class="stat-value">89</div>
          <div class="stat-label">Active Sessions</div>
        </div>
        <div class="stat">
          <div class="stat-value">456</div>
          <div class="stat-label">New This Month</div>
        </div>
      </div>
    </Card>

    <Card variant="elevated">
      {#snippet header()}
        <h3>🎯 Quick Actions</h3>
      {/snippet}

      <div class="actions">
        <Button onclick={handleNotificationTest} variant="primary">
          Test Notification
        </Button>
        <Button onclick={handleThemeToggle} variant="outline">
          Toggle Theme
        </Button>
        <Button variant="outline">
          View Reports
        </Button>
      </div>
    </Card>

    <Card variant="outlined">
      {#snippet header()}
        <h3>📈 Recent Activity</h3>
      {/snippet}

      <div class="activity">
        <div class="activity-item">
          <div class="activity-icon">👤</div>
          <div class="activity-content">
            <div class="activity-title">New user registered</div>
            <div class="activity-time">2 minutes ago</div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-icon">📝</div>
          <div class="activity-content">
            <div class="activity-title">Report generated</div>
            <div class="activity-time">1 hour ago</div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-icon">🔧</div>
          <div class="activity-content">
            <div class="activity-title">System maintenance completed</div>
            <div class="activity-time">3 hours ago</div>
          </div>
        </div>
      </div>
    </Card>

    {#if user}
      <Card variant="elevated">
        {#snippet header()}
          <h3>👋 User Profile</h3>
        {/snippet}

        <div class="profile">
          <div class="profile-info">
            <strong>{user.name}</strong>
            <div class="profile-email">{user.email}</div>
            <div class="profile-meta">
              Joined {new Date(user.created_at).toLocaleDateString()}
            </div>
          </div>
          
          <Button variant="outline" size="sm">
            Edit Profile
          </Button>
        </div>
      </Card>
    {/if}
  </div>
</div>

<style>
  .dashboard {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .dashboard-header {
    margin-bottom: 2rem;
  }

  .dashboard-header h1 {
    margin: 0 0 0.5rem;
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
  }

  .subtitle {
    margin: 0;
    color: #6b7280;
    font-size: 1rem;
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .stats {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }

  .stat {
    text-align: center;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary-color, #ff3e00);
  }

  .stat-label {
    font-size: 0.875rem;
    color: #6b7280;
    margin-top: 0.25rem;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .activity {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .activity-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .activity-icon {
    font-size: 1.25rem;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f3f4f6;
    border-radius: 50%;
  }

  .activity-title {
    font-weight: 500;
    color: #111827;
  }

  .activity-time {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .profile {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }

  .profile-info {
    flex: 1;
  }

  .profile-email {
    color: #6b7280;
    font-size: 0.875rem;
    margin-top: 0.25rem;
  }

  .profile-meta {
    color: #9ca3af;
    font-size: 0.75rem;
    margin-top: 0.5rem;
  }

  @media (max-width: 768px) {
    .dashboard {
      padding: 1rem;
    }

    .dashboard-grid {
      grid-template-columns: 1fr;
    }

    .stats {
      flex-direction: column;
      text-align: left;
    }

    .profile {
      flex-direction: column;
      align-items: stretch;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "(app)" / "dashboard" / "+page.svelte").write_text(dashboard_page)
        
        # Create app layout
        app_layout = '''<script lang="ts">
  import { globalStore } from '$stores';
  import type { LayoutData } from './$types.js';
  import type { Snippet } from 'svelte';

  interface Props {
    data: LayoutData;
    children: Snippet;
  }

  let { data, children }: Props = $props();

  let sidebarOpen = $state(false);

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/users', label: 'Users', icon: '👥' },
    { href: '/settings', label: 'Settings', icon: '⚙️' },
    { href: '/profile', label: 'Profile', icon: '👤' },
  ];

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }

  function handleLogout() {
    // Handle logout logic
    window.location.href = '/login';
  }
</script>

<div class="app-layout">
  <!-- Sidebar -->
  <aside class="sidebar" class:open={sidebarOpen}>
    <div class="sidebar-header">
      <h2>🚀 SvelteKit</h2>
      <button class="sidebar-toggle" onclick={toggleSidebar}>
        ✕
      </button>
    </div>
    
    <nav class="sidebar-nav">
      {#each navItems as { href, label, icon }}
        <a href={href} class="nav-item">
          <span class="nav-icon">{icon}</span>
          <span class="nav-label">{label}</span>
        </a>
      {/each}
    </nav>
    
    <div class="sidebar-footer">
      <button class="logout-btn" onclick={handleLogout}>
        <span class="nav-icon">🚪</span>
        <span class="nav-label">Logout</span>
      </button>
    </div>
  </aside>

  <!-- Main content -->
  <div class="main-content">
    <header class="app-header">
      <button class="sidebar-toggle mobile-only" onclick={toggleSidebar}>
        ☰
      </button>
      
      <div class="header-title">
        <h1>Welcome to your App</h1>
      </div>
      
      <div class="header-actions">
        <button class="notification-btn">
          🔔
        </button>
        
        <div class="user-menu">
          <button class="user-btn">
            👤 {data.user?.name || 'User'}
          </button>
        </div>
      </div>
    </header>

    <main class="content">
      {@render children()}
    </main>
  </div>

  <!-- Sidebar overlay for mobile -->
  {#if sidebarOpen}
    <div class="sidebar-overlay" onclick={toggleSidebar}></div>
  {/if}
</div>

<style>
  .app-layout {
    display: flex;
    min-height: 100vh;
    background: #f9fafb;
  }

  .sidebar {
    width: 250px;
    background: white;
    border-right: 1px solid #e5e7eb;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: -250px;
    height: 100vh;
    transition: left 0.3s ease;
    z-index: 200;
  }

  .sidebar.open {
    left: 0;
  }

  .sidebar-header {
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .sidebar-header h2 {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--primary-color, #ff3e00);
  }

  .sidebar-toggle {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: #6b7280;
    padding: 0.25rem;
    border-radius: 4px;
  }

  .sidebar-toggle:hover {
    background: #f3f4f6;
  }

  .sidebar-nav {
    flex: 1;
    padding: 1rem 0;
  }

  .nav-item,
  .logout-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: #374151;
    text-decoration: none;
    transition: background-color 0.2s ease;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-size: 1rem;
  }

  .nav-item:hover,
  .logout-btn:hover {
    background: #f3f4f6;
  }

  .nav-item.active {
    background: #f3f4f6;
    color: var(--primary-color, #ff3e00);
  }

  .nav-icon {
    font-size: 1.125rem;
  }

  .nav-label {
    font-weight: 500;
  }

  .sidebar-footer {
    border-top: 1px solid #e5e7eb;
    padding: 1rem 0;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-left: 0;
  }

  .app-header {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 0 1.5rem;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .header-title {
    flex: 1;
  }

  .header-title h1 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .notification-btn,
  .user-btn {
    background: none;
    border: none;
    padding: 0.5rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .notification-btn:hover,
  .user-btn:hover {
    background: #f3f4f6;
  }

  .content {
    flex: 1;
    overflow: auto;
  }

  .sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 100;
  }

  .mobile-only {
    display: none;
  }

  /* Desktop styles */
  @media (min-width: 1024px) {
    .sidebar {
      position: static;
      left: 0;
    }

    .sidebar-overlay {
      display: none;
    }

    .sidebar-toggle {
      display: none;
    }

    .main-content {
      margin-left: 0;
    }
  }

  /* Mobile styles */
  @media (max-width: 1023px) {
    .mobile-only {
      display: block;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "(app)" / "+layout.svelte").write_text(app_layout)
        
        # Create minimal root layout (+layout.svelte)
        # This layout should be minimal since route groups have their own layouts
        layout = '''<script lang="ts">
  import type { LayoutData } from './$types.js';
  import type { Snippet } from 'svelte';

  interface Props {
    data: LayoutData;
    children: Snippet;
  }

  let { data, children }: Props = $props();
</script>

<!-- Root layout - minimal wrapper for all routes -->
<div class="app">
  {@render children()}
</div>

<style>
  .app {
    min-height: 100vh;
  }

  /* Global app styles */
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: #fafafa;
    color: #333;
  }

  :global(*) {
    box-sizing: border-box;
  }
</style>
'''
        (self.frontend_dir / "src" / "routes" / "+layout.svelte").write_text(layout)
        
        # Create app.css
        app_css = '''/* Global styles for the SvelteKit app */

:root {
  --primary-color: #ff3e00;
  --secondary-color: #007acc;
  --text-color: #333;
  --bg-color: #fafafa;
  --border-color: #e0e0e0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: var(--bg-color);
  color: var(--text-color);
  line-height: 1.6;
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

/* Focus styles for accessibility */
*:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Button base styles */
button {
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
  border: none;
  background: transparent;
}

/* Link base styles */
a {
  color: inherit;
  text-decoration: none;
}

/* Input base styles */
input, textarea {
  font-family: inherit;
  font-size: inherit;
}
'''
        (self.frontend_dir / "src" / "app.css").write_text(app_css)