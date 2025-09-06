"""
Svelte Layout Components Generator
Handles creation of layout and structural components like Header, Sidebar, Footer, etc.
"""

from pathlib import Path
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name


class SvelteLayoutsGenerator(BaseSvelteGenerator):
    """Generator for Svelte layout components"""
    
    def create_layout_components(self) -> None:
        """Create all layout components."""
        print("  🏗️ Creating Svelte layout components...")
        
        # Create individual layout components
        self._create_header_component()
        self._create_sidebar_component()
        self._create_footer_component()
        
        print("  ✓ Svelte layout components created")
    
    def _create_header_component(self) -> None:
        """Create Header component."""
        header_component = '''<script lang="ts">
  import { Button } from '$components/ui';
  import { authState, logout } from '$lib/stores/auth.svelte';
  import type { User } from '$lib/types/auth';

  interface Props {
    title?: string;
    showAuth?: boolean;
    onMenuClick?: () => void;
  }

  let { title, showAuth = true, onMenuClick }: Props = $props();
  
  // Access auth state directly from runes
  const user = $derived(authState.user);
  const isAuthenticated = $derived(authState.isAuthenticated);

  function handleLogout() {
    logout();
  }

  function handleProfileClick() {
    // Navigate to profile page
    window.location.href = '/profile';
  }
</script>

<header class="header">
  <div class="header-content">
    <!-- Mobile menu button -->
    {#if onMenuClick}
      <button class="menu-button" onclick={onMenuClick} aria-label="Toggle menu">
        <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    {/if}

    <!-- Logo/Title -->
    <div class="logo-section">
      <a href="/" class="logo-link">
        {#if title}
          <h1 class="logo-text">{title}</h1>
        {:else}
          <h1 class="logo-text">''' + self.project_name.replace('_', ' ').title() + '''</h1>
        {/if}
      </a>
    </div>

    <!-- Navigation -->
    <nav class="nav-section">
      <div class="nav-links">
        <a href="/" class="nav-link">Home</a>
        {#if isAuthenticated}
          <a href="/dashboard" class="nav-link">Dashboard</a>
        {/if}
        <a href="/about" class="nav-link">About</a>
        <a href="/contact" class="nav-link">Contact</a>
      </div>
    </nav>

    <!-- Auth section -->
    {#if showAuth}
      <div class="auth-section">
        {#if isAuthenticated && user}
          <div class="user-menu">
            <button class="user-button" onclick={handleProfileClick}>
              <div class="user-info">
                <span class="user-name">{user.name}</span>
                <span class="user-role">{user.role}</span>
              </div>
              {#if user.avatar}
                <img src={user.avatar} alt={user.name} class="avatar" />
              {:else}
                <div class="avatar-placeholder">
                  {user.name.charAt(0).toUpperCase()}
                </div>
              {/if}
            </button>
            <Button variant="outline" size="sm" onclick={handleLogout}>
              Logout
            </Button>
          </div>
        {:else}
          <div class="auth-buttons">
            <Button variant="ghost" size="sm">
              <a href="/login" class="auth-link">Login</a>
            </Button>
            <Button variant="primary" size="sm">
              <a href="/register" class="auth-link">Sign Up</a>
            </Button>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</header>

<style>
  .header {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  }

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 4rem;
  }

  .menu-button {
    display: none;
    background: none;
    border: none;
    padding: 0.5rem;
    border-radius: 6px;
    color: #6b7280;
    cursor: pointer;
  }

  .menu-button:hover {
    background: #f3f4f6;
    color: #374151;
  }

  .menu-icon {
    width: 1.5rem;
    height: 1.5rem;
  }

  .logo-section {
    flex-shrink: 0;
  }

  .logo-link {
    text-decoration: none;
    color: inherit;
  }

  .logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color, #ff3e00);
    margin: 0;
  }

  .nav-section {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  .nav-links {
    display: flex;
    gap: 2rem;
  }

  .nav-link {
    color: #6b7280;
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 0;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
  }

  .nav-link:hover {
    color: var(--primary-color, #ff3e00);
    border-bottom-color: var(--primary-color, #ff3e00);
  }

  .auth-section {
    flex-shrink: 0;
  }

  .user-menu {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .user-button {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: none;
    border: 1px solid #e5e7eb;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .user-button:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
  }

  .user-info {
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  .user-name {
    font-weight: 500;
    color: #111827;
    font-size: 0.875rem;
  }

  .user-role {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: capitalize;
  }

  .avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    object-fit: cover;
  }

  .avatar-placeholder {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: var(--primary-color, #ff3e00);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
    font-size: 0.875rem;
  }

  .auth-buttons {
    display: flex;
    gap: 0.5rem;
  }

  .auth-link {
    color: inherit;
    text-decoration: none;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .menu-button {
      display: block;
    }

    .nav-section {
      display: none;
    }

    .user-info {
      display: none;
    }

    .auth-buttons {
      gap: 0.25rem;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Header" / "Header.svelte").write_text(header_component)
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Header" / "index.ts").write_text("export { default } from './Header.svelte';")
    
    def _create_sidebar_component(self) -> None:
        """Create Sidebar component."""
        sidebar_component = '''<script lang="ts">
  import { authState } from '$lib/stores/auth.svelte';
  import type { Snippet } from 'svelte';

  interface Props {
    open?: boolean;
    onClose?: () => void;
    children?: Snippet;
  }

  interface NavItem {
    label: string;
    href: string;
    icon?: string;
    requiresAuth?: boolean;
    adminOnly?: boolean;
  }

  let { open = false, onClose, children }: Props = $props();
  
  const user = $derived(authState.user);
  const isAuthenticated = $derived(authState.isAuthenticated);
  
  const navItems: NavItem[] = [
    { label: 'Home', href: '/', icon: '🏠' },
    { label: 'Dashboard', href: '/dashboard', icon: '📊', requiresAuth: true },
    { label: 'Profile', href: '/profile', icon: '👤', requiresAuth: true },
    { label: 'Settings', href: '/settings', icon: '⚙️', requiresAuth: true },
    { label: 'Admin', href: '/admin', icon: '🔐', requiresAuth: true, adminOnly: true },
    { label: 'About', href: '/about', icon: 'ℹ️' },
    { label: 'Contact', href: '/contact', icon: '📧' }
  ];

  function shouldShowItem(item: NavItem): boolean {
    if (item.requiresAuth && !isAuthenticated) return false;
    if (item.adminOnly && user?.role !== 'admin') return false;
    return true;
  }

  function handleItemClick() {
    onClose?.();
  }

  function handleBackdropClick() {
    onClose?.();
  }
</script>

{#if open}
  <!-- Mobile backdrop -->
  <div class="sidebar-backdrop" onclick={handleBackdropClick} aria-hidden="true"></div>
{/if}

<aside class="sidebar" class:open aria-label="Navigation sidebar">
  <div class="sidebar-content">
    <!-- Sidebar header -->
    <div class="sidebar-header">
      <h2 class="sidebar-title">Menu</h2>
      {#if onClose}
        <button class="close-button" onclick={onClose} aria-label="Close sidebar">
          ✕
        </button>
      {/if}
    </div>

    <!-- Navigation items -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        {#each navItems as item}
          {#if shouldShowItem(item)}
            <li class="nav-item">
              <a 
                href={item.href} 
                class="nav-link"
                onclick={handleItemClick}
              >
                {#if item.icon}
                  <span class="nav-icon">{item.icon}</span>
                {/if}
                <span class="nav-label">{item.label}</span>
              </a>
            </li>
          {/if}
        {/each}
      </ul>
    </nav>

    <!-- User section -->
    {#if isAuthenticated && user}
      <div class="user-section">
        <div class="user-card">
          <div class="user-avatar">
            {#if user.avatar}
              <img src={user.avatar} alt={user.name} class="avatar-image" />
            {:else}
              <div class="avatar-placeholder">
                {user.name.charAt(0).toUpperCase()}
              </div>
            {/if}
          </div>
          <div class="user-details">
            <div class="user-name">{user.name}</div>
            <div class="user-role">{user.role}</div>
          </div>
        </div>
      </div>
    {/if}

    <!-- Custom content slot -->
    {#if children}
      <div class="sidebar-footer">
        {@render children()}
      </div>
    {/if}
  </div>
</aside>

<style>
  .sidebar-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 40;
    display: none;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 16rem;
    background: white;
    border-right: 1px solid #e5e7eb;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 50;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .sidebar.open + .sidebar-backdrop {
    display: block;
  }

  .sidebar-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 1rem;
  }

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .sidebar-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin: 0;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
    padding: 0.25rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
  }

  .close-button:hover {
    background: #f3f4f6;
    color: #374151;
  }

  .sidebar-nav {
    flex: 1;
  }

  .nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .nav-item {
    margin: 0;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    color: #6b7280;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .nav-link:hover {
    background: #f3f4f6;
    color: #374151;
  }

  .nav-link.active {
    background: #fef2f2;
    color: var(--primary-color, #ff3e00);
  }

  .nav-icon {
    font-size: 1.25rem;
    width: 1.5rem;
    text-align: center;
  }

  .nav-label {
    flex: 1;
  }

  .user-section {
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .user-card {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: #f9fafb;
    border-radius: 8px;
  }

  .user-avatar {
    flex-shrink: 0;
  }

  .avatar-image {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    object-fit: cover;
  }

  .avatar-placeholder {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: var(--primary-color, #ff3e00);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1rem;
  }

  .user-details {
    flex: 1;
    min-width: 0;
  }

  .user-name {
    font-weight: 500;
    color: #111827;
    font-size: 0.875rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .user-role {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: capitalize;
  }

  .sidebar-footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  /* Desktop styles */
  @media (min-width: 1024px) {
    .sidebar {
      position: static;
      transform: none;
      box-shadow: none;
      border-right: 1px solid #e5e7eb;
    }

    .sidebar-backdrop {
      display: none !important;
    }

    .close-button {
      display: none;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Sidebar" / "Sidebar.svelte").write_text(sidebar_component)
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Sidebar" / "index.ts").write_text("export { default } from './Sidebar.svelte';")
    
    def _create_footer_component(self) -> None:
        """Create Footer component."""
        footer_component = '''<script lang="ts">
  interface Props {
    showSocial?: boolean;
    showNewsletter?: boolean;
    copyrightText?: string;
  }

  let { showSocial = true, showNewsletter = false, copyrightText }: Props = $props();
  
  const currentYear = new Date().getFullYear();
  const defaultCopyright = copyrightText || `© ${currentYear} ''' + self.project_name.replace('_', ' ').title() + '''. All rights reserved.`;

  // Newsletter signup state
  let email = $state('');
  let isSubscribing = $state(false);
  let subscribeMessage = $state('');

  async function handleNewsletterSubmit(event: Event) {
    event.preventDefault();
    if (!email.trim()) return;

    isSubscribing = true;
    subscribeMessage = '';

    try {
      // Simulate API call - replace with actual newsletter signup
      await new Promise(resolve => setTimeout(resolve, 1000));
      subscribeMessage = 'Thank you for subscribing!';
      email = '';
    } catch (error) {
      subscribeMessage = 'Something went wrong. Please try again.';
    } finally {
      isSubscribing = false;
    }
  }

  const socialLinks = [
    { name: 'Twitter', url: '#', icon: '🐦' },
    { name: 'GitHub', url: '#', icon: '🐱' },
    { name: 'LinkedIn', url: '#', icon: '💼' },
    { name: 'Email', url: 'mailto:contact@example.com', icon: '📧' }
  ];

  const footerLinks = {
    Product: [
      { name: 'Features', url: '/features' },
      { name: 'Pricing', url: '/pricing' },
      { name: 'API', url: '/api' },
      { name: 'Status', url: '/status' }
    ],
    Company: [
      { name: 'About', url: '/about' },
      { name: 'Blog', url: '/blog' },
      { name: 'Careers', url: '/careers' },
      { name: 'Contact', url: '/contact' }
    ],
    Support: [
      { name: 'Help Center', url: '/help' },
      { name: 'Documentation', url: '/docs' },
      { name: 'Community', url: '/community' },
      { name: 'Updates', url: '/updates' }
    ],
    Legal: [
      { name: 'Privacy', url: '/privacy' },
      { name: 'Terms', url: '/terms' },
      { name: 'Cookies', url: '/cookies' },
      { name: 'Licenses', url: '/licenses' }
    ]
  };
</script>

<footer class="footer">
  <div class="footer-content">
    <!-- Main footer content -->
    <div class="footer-main">
      <!-- Company info -->
      <div class="footer-section company-section">
        <h3 class="footer-title">''' + self.project_name.replace('_', ' ').title() + '''</h3>
        <p class="company-description">
          Building amazing experiences with modern web technologies. 
          Fast, reliable, and user-friendly applications for everyone.
        </p>
        
        {#if showSocial}
          <div class="social-links">
            {#each socialLinks as social}
              <a 
                href={social.url} 
                class="social-link" 
                aria-label={social.name}
                target="_blank"
                rel="noopener noreferrer"
              >
                <span class="social-icon">{social.icon}</span>
              </a>
            {/each}
          </div>
        {/if}
      </div>

      <!-- Links sections -->
      {#each Object.entries(footerLinks) as [category, links]}
        <div class="footer-section">
          <h4 class="section-title">{category}</h4>
          <ul class="link-list">
            {#each links as link}
              <li class="link-item">
                <a href={link.url} class="footer-link">
                  {link.name}
                </a>
              </li>
            {/each}
          </ul>
        </div>
      {/each}

      <!-- Newsletter signup -->
      {#if showNewsletter}
        <div class="footer-section newsletter-section">
          <h4 class="section-title">Stay Updated</h4>
          <p class="newsletter-description">
            Get the latest news and updates delivered to your inbox.
          </p>
          
          <form onsubmit={handleNewsletterSubmit} class="newsletter-form">
            <div class="newsletter-input-group">
              <input
                type="email"
                bind:value={email}
                placeholder="Enter your email"
                class="newsletter-input"
                required
                disabled={isSubscribing}
              />
              <button 
                type="submit" 
                class="newsletter-button"
                disabled={isSubscribing || !email.trim()}
              >
                {isSubscribing ? 'Subscribing...' : 'Subscribe'}
              </button>
            </div>
            {#if subscribeMessage}
              <p class="newsletter-message" class:success={subscribeMessage.includes('Thank')}>
                {subscribeMessage}
              </p>
            {/if}
          </form>
        </div>
      {/if}
    </div>

    <!-- Footer bottom -->
    <div class="footer-bottom">
      <div class="footer-bottom-content">
        <p class="copyright">{defaultCopyright}</p>
        <div class="footer-meta">
          <span class="build-info">Built with SvelteKit</span>
          <span class="version">v1.0.0</span>
        </div>
      </div>
    </div>
  </div>
</footer>

<style>
  .footer {
    background: #1f2937;
    color: #e5e7eb;
    margin-top: auto;
  }

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 1rem 0;
  }

  .footer-main {
    display: grid;
    grid-template-columns: 2fr repeat(4, 1fr);
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .footer-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .company-section {
    max-width: 300px;
  }

  .footer-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color, #ff3e00);
    margin: 0 0 1rem 0;
  }

  .company-description {
    color: #9ca3af;
    line-height: 1.6;
    margin: 0 0 1.5rem 0;
  }

  .social-links {
    display: flex;
    gap: 0.75rem;
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    background: #374151;
    border-radius: 6px;
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .social-link:hover {
    background: var(--primary-color, #ff3e00);
    transform: translateY(-2px);
  }

  .social-icon {
    font-size: 1.25rem;
  }

  .section-title {
    font-size: 1rem;
    font-weight: 600;
    color: white;
    margin: 0 0 1rem 0;
  }

  .link-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .link-item {
    margin: 0;
  }

  .footer-link {
    color: #9ca3af;
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.2s ease;
  }

  .footer-link:hover {
    color: var(--primary-color, #ff3e00);
  }

  .newsletter-section {
    max-width: 300px;
  }

  .newsletter-description {
    color: #9ca3af;
    font-size: 0.875rem;
    line-height: 1.5;
    margin: 0 0 1rem 0;
  }

  .newsletter-form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .newsletter-input-group {
    display: flex;
    gap: 0.5rem;
  }

  .newsletter-input {
    flex: 1;
    padding: 0.5rem 0.75rem;
    background: #374151;
    border: 1px solid #4b5563;
    border-radius: 6px;
    color: white;
    font-size: 0.875rem;
  }

  .newsletter-input::placeholder {
    color: #9ca3af;
  }

  .newsletter-input:focus {
    outline: none;
    border-color: var(--primary-color, #ff3e00);
  }

  .newsletter-button {
    padding: 0.5rem 1rem;
    background: var(--primary-color, #ff3e00);
    border: none;
    border-radius: 6px;
    color: white;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease;
    white-space: nowrap;
  }

  .newsletter-button:hover:not(:disabled) {
    background: #d63200;
  }

  .newsletter-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .newsletter-message {
    font-size: 0.75rem;
    margin: 0;
    color: #ef4444;
  }

  .newsletter-message.success {
    color: #10b981;
  }

  .footer-bottom {
    border-top: 1px solid #374151;
    padding: 1.5rem 0;
  }

  .footer-bottom-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .copyright {
    color: #9ca3af;
    font-size: 0.875rem;
    margin: 0;
  }

  .footer-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.75rem;
    color: #6b7280;
  }

  .build-info,
  .version {
    display: flex;
    align-items: center;
  }

  /* Mobile responsive */
  @media (max-width: 1024px) {
    .footer-main {
      grid-template-columns: repeat(2, 1fr);
    }

    .company-section {
      grid-column: 1 / -1;
      max-width: none;
    }

    .newsletter-section {
      grid-column: 1 / -1;
      max-width: none;
    }
  }

  @media (max-width: 640px) {
    .footer-main {
      grid-template-columns: 1fr;
      gap: 2rem;
    }

    .footer-bottom-content {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .newsletter-input-group {
      flex-direction: column;
    }
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Footer" / "Footer.svelte").write_text(footer_component)
        (self.frontend_dir / "src" / "lib" / "components" / "layout" / "Footer" / "index.ts").write_text("export { default } from './Footer.svelte';")