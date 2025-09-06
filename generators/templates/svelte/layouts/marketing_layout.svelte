<script lang="ts">
  import type { LayoutData } from './$types.js';
  import type { Snippet } from 'svelte';

  interface Props {
    data: LayoutData;
    children: Snippet;
  }

  let { data, children }: Props = $props();

  const navItems = [
    { href: '/', label: 'Home', icon: '🏠' },
    { href: '/about', label: 'About', icon: 'ℹ️' },
    { href: '/pricing', label: 'Pricing', icon: '💰' },
    { href: '/contact', label: 'Contact', icon: '📞' },
    { href: '/login', label: 'Login', icon: '🔐' },
  ];
</script>

<div class="marketing-layout">
  <header class="header">
    <nav class="nav">
      <div class="nav-brand">
        <h2>🚀 {data.siteName || '{{APP_NAME}}'}</h2>
      </div>

      <ul class="nav-links">
        {#each navItems as { href, label, icon }}
          <li>
            <a href={href} class="nav-link">
              {icon} {label}
            </a>
          </li>
        {/each}
      </ul>
    </nav>
  </header>

  <main class="main">
    {@render children()}
  </main>

  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Product</h3>
        <ul>
          <li><a href="/features">Features</a></li>
          <li><a href="/pricing">Pricing</a></li>
          <li><a href="/docs">Documentation</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h3>Company</h3>
        <ul>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/careers">Careers</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h3>Legal</h3>
        <ul>
          <li><a href="/privacy">Privacy</a></li>
          <li><a href="/terms">Terms</a></li>
          <li><a href="/cookies">Cookies</a></li>
        </ul>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2024 {{APP_NAME}}. All rights reserved.</p>
    </div>
  </footer>
</div>

<style>
  .marketing-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .header {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1rem;
    height: 64px;
  }

  .nav-brand h2 {
    margin: 0;
    color: var(--primary-color, #ff3e00);
    font-size: 1.25rem;
  }

  .nav-links {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 1.5rem;
  }

  .nav-link {
    text-decoration: none;
    color: #374151;
    font-weight: 500;
    padding: 0.5rem 0;
    transition: color 0.2s ease;
  }

  .nav-link:hover {
    color: var(--primary-color, #ff3e00);
  }

  .main {
    flex: 1;
  }

  .footer {
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
    padding: 3rem 0 1rem;
  }

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
  }

  .footer-section h3 {
    margin: 0 0 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #111827;
  }

  .footer-section ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .footer-section li {
    margin-bottom: 0.5rem;
  }

  .footer-section a {
    text-decoration: none;
    color: #6b7280;
    font-size: 0.875rem;
    transition: color 0.2s ease;
  }

  .footer-section a:hover {
    color: var(--primary-color, #ff3e00);
  }

  .footer-bottom {
    max-width: 1200px;
    margin: 2rem auto 0;
    padding: 1rem;
    text-align: center;
    border-top: 1px solid #e5e7eb;
  }

  .footer-bottom p {
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
  }

  @media (max-width: 768px) {
    .nav {
      flex-direction: column;
      height: auto;
      padding: 1rem;
      gap: 1rem;
    }

    .nav-links {
      gap: 1rem;
    }

    .footer-content {
      grid-template-columns: 1fr;
      text-align: center;
    }
  }
</style>