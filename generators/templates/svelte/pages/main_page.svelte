<script lang="ts">
  import { useUserData } from '$composables/useUserData.svelte.js';
  import { Card } from '$components/ui';
  import type { PageData } from './$types.js';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let { user, loading } = useUserData(data.userId);

  let count = $state(0);
  let doubled = $derived(count * 2);

  function increment() {
    count += 1;
  }
</script>

<svelte:head>
  <title>Welcome to {{PROJECT_TITLE}}</title>
  <meta name="description" content="Modern SvelteKit app with Svelte 5 runes" />
</svelte:head>

<div class="container">
  <h1>🚀 Welcome to {{PROJECT_TITLE}}</h1>
  <p class="subtitle">Built with SvelteKit + Svelte 5 Runes + TypeScript</p>

  <div class="features">
    <Card variant="elevated">
      {#snippet header()}
        <h3>✨ Svelte 5 Runes</h3>
      {/snippet}

      <p>Modern reactive state management with explicit reactivity.</p>
      <div class="demo">
        <p>Count: {count}</p>
        <p>Doubled: {doubled}</p>
        <button onclick={increment}>Increment</button>
      </div>
    </Card>

    <Card variant="elevated">
      {#snippet header()}
        <h3>🔄 User Data</h3>
      {/snippet}

      {#if loading}
        <div class="loading">Loading user data...</div>
      {:else if user}
        <div class="user-info">
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>ID:</strong> {user.id}</p>
        </div>
      {:else}
        <p>No user data available</p>
      {/if}
    </Card>

    <Card variant="outlined">
      {#snippet header()}
        <h3>🌐 API Integration</h3>
      {/snippet}

      <p>Connected to FastAPI backend at:</p>
      <code>{data.apiUrl}</code>
    </Card>
  </div>
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    color: #ff3e00;
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 3rem;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .demo {
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 4px;
    margin-top: 1rem;
  }

  .demo button {
    background: #ff3e00;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 0.5rem;
  }

  .demo button:hover {
    background: #d63200;
  }

  .loading {
    color: #007acc;
    font-style: italic;
  }

  .user-info {
    background: #e8f5e8;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 0.5rem;
  }

  code {
    background: #f0f0f0;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: monospace;
  }
</style>