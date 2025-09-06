# Svelte 5 & SvelteKit Patterns Guide for LLMs

## CORRECT Patterns

### 1. Svelte 5 Runes (Reusable Logic)
```svelte
<!-- UserProfile.svelte -->
<script lang="ts">
  import { useUserData } from '$lib/composables/useUserData.js';
  
  interface Props {
    userId: string;
  }
  
  let { userId }: Props = $props();
  let { user, loading } = useUserData(userId);
</script>

{#if loading}
  <div>Loading...</div>
{:else if user}
  <div>{user.name}</div>
{/if}
```

```ts
// lib/composables/useUserData.ts
import { fetchUser } from '$lib/api';

export function useUserData(userId: string) {
  let user = $state<{ id: number; name: string } | null>(null);
  let loading = $state(true);
  
  $effect(() => {
    loading = true;
    fetchUser(userId).then(data => {
      user = data;
      loading = false;
    });
  });
  
  return {
    get user() { return user; },
    get loading() { return loading; }
  };
}
```

---

### 2. Component Composition (Slots + Snippets)
```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  
  interface Props {
    children: Snippet;
    header?: Snippet;
  }
  
  let { children, header }: Props = $props();
</script>

<div class="card">
  {#if header}
    <div class="card-header">
      {@render header()}
    </div>
  {/if}
  <div class="card-body">
    {@render children()}
  </div>
</div>
```

```svelte
<!-- Usage -->
<Card>
  {#snippet header()}
    <h2>Title</h2>
  {/snippet}
  
  <p>Content goes here</p>
</Card>
```

---

### 3. Container / Presentational Split
```svelte
<!-- UserListContainer.svelte -->
<script lang="ts">
  import { useUsers } from '$lib/composables/useUsers.js';
  import UserList from './UserList.svelte';
  
  let { users, loading } = useUsers();
</script>

<UserList {users} {loading} />
```

```svelte
<!-- UserList.svelte -->
<script lang="ts">
  interface User {
    id: number;
    name: string;
  }
  
  interface Props {
    users: User[];
    loading: boolean;
  }
  
  let { users, loading }: Props = $props();
</script>

{#if loading}
  <div>Loading...</div>
{:else}
  <ul>
    {#each users as user (user.id)}
      <li>{user.name}</li>
    {/each}
  </ul>
{/if}
```

---

### 4. SvelteKit Form Actions
```svelte
<!-- routes/users/[id]/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { PageData, ActionData } from './$types.js';
  
  interface Props {
    data: PageData;
    form: ActionData;
  }
  
  let { data, form }: Props = $props();
</script>

<form method="POST" action="?/updateUser" use:enhance>
  <input name="name" value={data.user.name} />
  <button type="submit">Update</button>
</form>

{#if form?.error}
  <p class="error">{form.error}</p>
{/if}
```

```ts
// routes/users/[id]/+page.server.ts
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ params }) => {
  const user = await getUserById(params.id);
  return { user };
};

export const actions: Actions = {
  updateUser: async ({ request, params }) => {
    const data = await request.formData();
    const name = data.get('name') as string;
    
    try {
      await updateUser(params.id, { name });
      return { success: true };
    } catch (error) {
      return fail(400, { error: 'Failed to update user' });
    }
  }
};
```

---

### 5. Optimistic Updates with Stores
```svelte
<!-- TodoList.svelte -->
<script lang="ts">
  import { todoStore } from '$lib/stores/todos.js';
  
  let newTodoText = $state('');
  
  async function addTodo() {
    if (!newTodoText.trim()) return;
    
    const tempId = Date.now();
    todoStore.addOptimistic({ id: tempId, text: newTodoText, pending: true });
    
    try {
      const savedTodo = await createTodo(newTodoText);
      todoStore.confirmOptimistic(tempId, savedTodo);
      newTodoText = '';
    } catch (error) {
      todoStore.removeOptimistic(tempId);
    }
  }
</script>

<form onsubmit={addTodo}>
  <input bind:value={newTodoText} />
  <button type="submit">Add Todo</button>
</form>

{#each $todoStore as todo (todo.id)}
  <div class:pending={todo.pending}>
    {todo.text}
  </div>
{/each}
```

```ts
// lib/stores/todos.ts
import { writable } from 'svelte/store';

interface Todo {
  id: number;
  text: string;
  pending?: boolean;
}

function createTodoStore() {
  const { subscribe, update } = writable<Todo[]>([]);
  
  return {
    subscribe,
    addOptimistic: (todo: Todo) => update(todos => [...todos, todo]),
    confirmOptimistic: (tempId: number, realTodo: Todo) => 
      update(todos => todos.map(t => t.id === tempId ? realTodo : t)),
    removeOptimistic: (tempId: number) =>
      update(todos => todos.filter(t => t.id !== tempId))
  };
}

export const todoStore = createTodoStore();
```

---

### 6. Error Boundaries (Svelte 5)
```svelte
<!-- ErrorBoundary.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  
  interface Props {
    children: Snippet;
    fallback?: Snippet<[Error]>;
  }
  
  let { children, fallback }: Props = $props();
  let error = $state<Error | null>(null);
  
  function handleError(event: ErrorEvent) {
    error = event.error;
  }
</script>

<svelte:window onerror={handleError} />

{#if error}
  {#if fallback}
    {@render fallback(error)}
  {:else}
    <div class="error">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
    </div>
  {/if}
{:else}
  {@render children()}
{/if}
```

---

### 7. Element References and Actions
```svelte
<!-- FocusButton.svelte -->
<script lang="ts">
  import type { Action } from 'svelte/action';
  
  const focusOnMount: Action<HTMLElement> = (node) => {
    node.focus();
    
    return {
      destroy() {
        // cleanup if needed
      }
    };
  };
</script>

<button use:focusOnMount>
  <slot />
</button>
```

---

### 8. Reactive State Management (Svelte 5)
```svelte
<!-- UserSearch.svelte -->
<script lang="ts">
  import { searchUsers } from '$lib/api';
  import { debounce } from '$lib/utils';
  
  let searchTerm = $state('');
  let results = $state<User[]>([]);
  let loading = $state(false);
  
  // Derived value
  let hasResults = $derived(results.length > 0);
  
  // Debounced search effect
  $effect(() => {
    if (!searchTerm.trim()) {
      results = [];
      return;
    }
    
    loading = true;
    const debouncedSearch = debounce(async () => {
      try {
        results = await searchUsers(searchTerm);
      } finally {
        loading = false;
      }
    }, 300);
    
    debouncedSearch();
  });
</script>

<input bind:value={searchTerm} placeholder="Search users..." />

{#if loading}
  <div>Searching...</div>
{:else if hasResults}
  <ul>
    {#each results as user (user.id)}
      <li>{user.name}</li>
    {/each}
  </ul>
{:else if searchTerm}
  <div>No results found</div>
{/if}
```

---

## ANTIPATTERNS to Avoid

### 1. Array Index as Keys
```svelte
<!-- DON'T: Use array index as key -->
{#each todos as todo, i (i)}
  <li>{todo.text}</li>
{/each}

<!-- DO: Use stable unique IDs -->
{#each todos as todo (todo.id)}
  <li>{todo.text}</li>
{/each}
```

### 2. Direct State Mutation (Svelte 4)
```svelte
<!-- DON'T: Mutate arrays/objects directly -->
<script>
  let todos = [];
  
  function addTodo(text) {
    todos.push({ id: Date.now(), text }); // ❌ Direct mutation
    todos = todos; // ❌ Manual reactivity trigger
  }
</script>

<!-- DO: Create new arrays/objects -->
<script>
  let todos = [];
  
  function addTodo(text) {
    todos = [...todos, { id: Date.now(), text }]; // ✅ New array
  }
</script>
```

### 3. Reactive Statement Abuse
```svelte
<!-- DON'T: Overuse reactive statements -->
<script>
  let count = 0;
  let doubled = 0;
  let quadrupled = 0;
  
  $: doubled = count * 2; // ❌ Simple calculation
  $: quadrupled = doubled * 2; // ❌ Dependent on reactive statement
  $: console.log(count); // ❌ Side effects in reactive statements
</script>

<!-- DO: Use derived values (Svelte 5) or computed properties -->
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
  let quadrupled = $derived(doubled * 2);
  
  $effect(() => {
    console.log(count); // ✅ Side effects in effects
  });
</script>
```

### 4. Massive Components
```svelte
<!-- DON'T: 500+ line components with mixed concerns -->
<script>
  // ❌ Hundreds of lines of mixed logic
  let users = [];
  let posts = [];
  let comments = [];
  // ... 400+ more lines
</script>

<!-- Massive template with everything -->

<!-- DO: Break into focused components -->
<script>
  import UserList from './UserList.svelte';
  import PostList from './PostList.svelte';
  import CommentList from './CommentList.svelte';
</script>

<UserList />
<PostList />
<CommentList />
```

### 5. Missing Prop Types
```svelte
<!-- DON'T: No prop validation -->
<script>
  export let user; // ❌ No type information
  export let onClick; // ❌ No type information
</script>

<!-- DO: Use TypeScript -->
<script lang="ts">
  interface User {
    id: number;
    name: string;
  }
  
  interface Props {
    user: User;
    onClick: () => void;
  }
  
  let { user, onClick }: Props = $props();
</script>
```

### 6. Excessive Prop Drilling
```svelte
<!-- DON'T: Pass props through many levels -->
<!-- App.svelte -->
<Layout {user} />

<!-- Layout.svelte -->
<Sidebar {user} /> <!-- ❌ Passing through -->

<!-- Sidebar.svelte -->
<UserMenu {user} /> <!-- ❌ Passing through -->

<!-- DO: Use context for deeply nested data -->
<!-- App.svelte -->
<script>
  import { setContext } from 'svelte';
  setContext('user', user);
</script>
<Layout />

<!-- UserMenu.svelte -->
<script>
  import { getContext } from 'svelte';
  const user = getContext('user'); // ✅ Direct access
</script>
```

### 7. Direct DOM Manipulation
```svelte
<!-- DON'T: Manual DOM manipulation -->
<script>
  import { onMount } from 'svelte';
  
  onMount(() => {
    document.getElementById('myDiv').style.color = 'red'; // ❌ Direct DOM
  });
</script>

<div id="myDiv">Hello</div>

<!-- DO: Use Svelte's reactivity -->
<script>
  let isRed = $state(true);
</script>

<div class:red={isRed}>Hello</div>

<style>
  .red { color: red; }
</style>
```

### 8. Inefficient Event Handlers
```svelte
<!-- DON'T: Create functions in markup -->
{#each items as item (item.id)}
  <button onclick={() => deleteItem(item.id)}> <!-- ❌ New function each render -->
    Delete
  </button>
{/each}

<!-- DO: Use stable references -->
<script>
  function handleDelete(id: number) {
    return () => deleteItem(id);
  }
</script>

{#each items as item (item.id)}
  <button onclick={handleDelete(item.id)}> <!-- ✅ Stable reference -->
    Delete
  </button>
{/each}
```

---

## Common Linting / TypeScript Practices

### TypeScript Integration
```svelte
<script lang="ts">
  // ✅ Explicit interfaces
  interface User {
    id: number;
    name: string;
    email?: string;
  }
  
  interface Props {
    users: User[];
    onSelect: (user: User) => void;
  }
  
  let { users, onSelect }: Props = $props();
  
  // ✅ Typed functions
  function selectUser(user: User): void {
    onSelect(user);
  }
</script>
```

### Safe Property Access
```svelte
<script lang="ts">
  interface Props {
    user?: User | null;
  }
  
  let { user }: Props = $props();
</script>

<!-- ✅ Safe access with optional chaining -->
<div>{user?.name ?? 'Anonymous'}</div>
<div>{user?.profile?.email ?? 'No email'}</div>
```

### Proper Store Types
```ts
// lib/stores/user.ts
import { writable } from 'svelte/store';

interface User {
  id: number;
  name: string;
}

interface UserState {
  current: User | null;
  loading: boolean;
  error: string | null;
}

export const userStore = writable<UserState>({
  current: null,
  loading: false,
  error: null
});
```

---

## SvelteKit-Specific Patterns

### 1. Data Loading
```ts
// routes/users/+page.server.ts
import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ url, depends }) => {
  const page = Number(url.searchParams.get('page')) || 1;
  
  depends('users:list');
  
  const users = await getUsersPaginated(page);
  
  return {
    users,
    pagination: {
      page,
      hasNext: users.length === 10
    }
  };
};
```

### 2. Universal Load Functions
```ts
// routes/posts/[slug]/+page.ts
import type { PageLoad } from './$types.js';

export const load: PageLoad = async ({ params, fetch }) => {
  const [post, comments] = await Promise.all([
    fetch(`/api/posts/${params.slug}`).then(r => r.json()),
    fetch(`/api/posts/${params.slug}/comments`).then(r => r.json())
  ]);
  
  return {
    post,
    comments
  };
};
```

### 3. Advanced Form Handling
```svelte
<!-- routes/contact/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import { invalidateAll } from '$app/navigation';
  import type { ActionData } from './$types.js';
  
  interface Props {
    form: ActionData;
  }
  
  let { form }: Props = $props();
  let submitting = $state(false);
</script>

<form 
  method="POST" 
  use:enhance={({ formData, cancel }) => {
    submitting = true;
    
    return async ({ result, update }) => {
      submitting = false;
      
      if (result.type === 'success') {
        await invalidateAll();
      }
      
      await update();
    };
  }}
>
  <input name="email" type="email" required />
  <textarea name="message" required></textarea>
  <button type="submit" disabled={submitting}>
    {submitting ? 'Sending...' : 'Send'}
  </button>
</form>

{#if form?.success}
  <p class="success">Message sent successfully!</p>
{/if}

{#if form?.errors}
  <ul class="errors">
    {#each Object.entries(form.errors) as [field, error]}
      <li>{field}: {error}</li>
    {/each}
  </ul>
{/if}
```

### 4. Server-Side Error Handling
```ts
// hooks.server.ts
import { error } from '@sveltejs/kit';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  try {
    return await resolve(event);
  } catch (err) {
    console.error('Server error:', err);
    throw error(500, 'Internal server error');
  }
};
```

---

## Performance Patterns

### 1. Lazy Loading Components
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  
  let HeavyComponent: any = $state(null);
  let showHeavy = $state(false);
  
  onMount(async () => {
    if (showHeavy) {
      const module = await import('./HeavyComponent.svelte');
      HeavyComponent = module.default;
    }
  });
</script>

<button onclick={() => showHeavy = !showHeavy}>
  Toggle Heavy Component
</button>

{#if showHeavy && HeavyComponent}
  <svelte:component this={HeavyComponent} />
{/if}
```

### 2. Virtual Lists for Large Data
```svelte
<!-- VirtualList.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  
  interface Props<T> {
    items: T[];
    itemHeight: number;
    containerHeight: number;
    children: Snippet<[T, number]>;
  }
  
  let { items, itemHeight, containerHeight, children }: Props<any> = $props();
  
  let scrollTop = $state(0);
  
  let visibleRange = $derived(() => {
    const start = Math.floor(scrollTop / itemHeight);
    const visible = Math.ceil(containerHeight / itemHeight);
    return {
      start: Math.max(0, start - 5),
      end: Math.min(items.length, start + visible + 5)
    };
  });
  
  let visibleItems = $derived(() => 
    items.slice(visibleRange.start, visibleRange.end)
  );
</script>

<div 
  class="virtual-list"
  style="height: {containerHeight}px; overflow-y: auto;"
  onscroll={(e) => scrollTop = e.currentTarget.scrollTop}
>
  <div style="height: {visibleRange.start * itemHeight}px;"></div>
  
  {#each visibleItems as item, index (item.id)}
    {@render children(item, visibleRange.start + index)}
  {/each}
  
  <div style="height: {(items.length - visibleRange.end) * itemHeight}px;"></div>
</div>
```

---

## Example: LLM Integration Composable
```ts
// lib/composables/useLlm.ts
import { writable } from 'svelte/store';

export function useLlm() {
  let output = $state('');
  let busy = $state(false);
  let error = $state<unknown>(null);
  let controller: AbortController | null = null;
  
  async function run(prompt: string) {
    error = null;
    busy = true;
    controller?.abort();
    controller = new AbortController();
    
    try {
      const res = await fetch('/api/llm', {
        method: 'POST',
        body: JSON.stringify({ prompt }),
        signal: controller.signal,
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      
      const { text } = await res.json();
      output = text;
    } catch (e: any) {
      if (e.name !== 'AbortError') {
        error = e;
      }
    } finally {
      busy = false;
    }
  }
  
  function cancel() {
    controller?.abort();
  }
  
  return {
    get output() { return output; },
    get busy() { return busy; },
    get error() { return error; },
    run,
    cancel
  };
}
```

```svelte
<!-- LlmForm.svelte -->
<script lang="ts">
  import { useLlm } from '$lib/composables/useLlm.js';
  
  let prompt = $state('');
  let { output, busy, error, run, cancel } = useLlm();
  
  async function handleSubmit() {
    if (prompt.trim()) {
      await run(prompt);
    }
  }
</script>

<form onsubmit={handleSubmit}>
  <textarea bind:value={prompt} placeholder="Enter your prompt..."></textarea>
  <div class="buttons">
    <button type="submit" disabled={busy}>
      {busy ? 'Running...' : 'Run'}
    </button>
    {#if busy}
      <button type="button" onclick={cancel}>Cancel</button>
    {/if}
  </div>
</form>

{#if error}
  <div class="error">Error: {String(error)}</div>
{:else if busy}
  <div class="loading">Processing...</div>
{:else if output}
  <pre class="output">{output}</pre>
{/if}

<style>
  .error { color: red; }
  .loading { color: blue; }
  .output { background: #f5f5f5; padding: 1rem; border-radius: 4px; }
  .buttons { display: flex; gap: 0.5rem; }
</style>
```

---

## Component Size Limits
- ✅ Max 200 lines per component
- ✅ Max 8 props per component  
- ✅ Single responsibility principle
- ✅ Break into smaller components when exceeding limits

## Svelte 5 Features to Embrace
- ✅ Runes ($state, $derived, $effect, $props)
- ✅ Snippets for flexible component composition
- ✅ Enhanced TypeScript support
- ✅ Improved reactivity system
- ✅ Better tree-shaking and performance

## SvelteKit Features to Use
- ✅ Form actions for server-side form handling
- ✅ Load functions for data fetching
- ✅ Hooks for request/response middleware  
- ✅ App stores for global state
- ✅ Service workers for offline support
- ✅ Advanced routing with layout groups