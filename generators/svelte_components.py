"""
Svelte UI Components Generator
Handles creation of reusable UI components like Card, Button, Input, Modal, etc.
"""

from pathlib import Path
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, frontend_dir: Path, project_name: str):
        self.frontend_dir = frontend_dir
        self.project_name = project_name


class SvelteComponentsGenerator(BaseSvelteGenerator):
    """Generator for Svelte UI components"""
    
    def create_ui_components(self) -> None:
        """Create all UI components."""
        print("  🎨 Creating Svelte UI components...")
        
        # Create individual UI components
        self._create_card_component()
        self._create_button_component()
        self._create_input_component()
        self._create_modal_component()
        
        print("  ✓ Svelte UI components created")
    
    def _create_card_component(self) -> None:
        """Create Card component."""
        card_component = '''<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    children: Snippet;
    header?: Snippet;
    footer?: Snippet;
    variant?: 'default' | 'outlined' | 'elevated';
  }

  let { children, header, footer, variant = 'default' }: Props = $props();
</script>

<div class="card" class:outlined={variant === 'outlined'} class:elevated={variant === 'elevated'}>
  {#if header}
    <div class="card-header">
      {@render header()}
    </div>
  {/if}

  <div class="card-body">
    {@render children()}
  </div>

  {#if footer}
    <div class="card-footer">
      {@render footer()}
    </div>
  {/if}
</div>

<style>
  .card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    transition: box-shadow 0.2s ease;
  }

  .card.outlined {
    border: 1px solid #e0e0e0;
  }

  .card.elevated {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .card.elevated:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }

  .card-header {
    padding: 1rem 1.5rem 0;
    border-bottom: 1px solid #f0f0f0;
  }

  .card-body {
    padding: 1.5rem;
  }

  .card-footer {
    padding: 0 1.5rem 1rem;
    border-top: 1px solid #f0f0f0;
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Card" / "Card.svelte").write_text(card_component)
        
        # Create Card barrel export
        card_index = '''export { default } from './Card.svelte';
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Card" / "index.ts").write_text(card_index)
    
    def _create_button_component(self) -> None:
        """Create Button component."""
        button_component = '''<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
    onclick?: () => void;
    children: Snippet;
  }

  import type { Snippet } from 'svelte';

  let { variant = 'primary', size = 'md', disabled = false, type = 'button', onclick, children }: Props = $props();
</script>

<button
  {type}
  {disabled}
  class="btn {variant} {size}"
  onclick={onclick}
>
  {@render children()}
</button>

<style>
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    font-weight: 500;
    border: 1px solid;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    font-family: inherit;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Sizes */
  .sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }

  .md {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }

  .lg {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
  }

  /* Variants */
  .primary {
    background: var(--primary-color, #ff3e00);
    border-color: var(--primary-color, #ff3e00);
    color: white;
  }

  .primary:hover:not(:disabled) {
    background: #d63200;
    border-color: #d63200;
  }

  .secondary {
    background: #6c757d;
    border-color: #6c757d;
    color: white;
  }

  .secondary:hover:not(:disabled) {
    background: #5a6268;
    border-color: #5a6268;
  }

  .outline {
    background: transparent;
    border-color: var(--primary-color, #ff3e00);
    color: var(--primary-color, #ff3e00);
  }

  .outline:hover:not(:disabled) {
    background: var(--primary-color, #ff3e00);
    color: white;
  }

  .ghost {
    background: transparent;
    border-color: transparent;
    color: var(--primary-color, #ff3e00);
  }

  .ghost:hover:not(:disabled) {
    background: rgba(255, 62, 0, 0.1);
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Button" / "Button.svelte").write_text(button_component)
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Button" / "index.ts").write_text("export { default } from './Button.svelte';")
    
    def _create_input_component(self) -> None:
        """Create Input component."""
        input_component = '''<script lang="ts">
  interface Props {
    type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
    placeholder?: string;
    value?: string;
    disabled?: boolean;
    required?: boolean;
    id?: string;
    name?: string;
    label?: string;
    error?: string;
    onchange?: (value: string) => void;
  }

  let { 
    type = 'text', 
    placeholder, 
    value = '', 
    disabled = false, 
    required = false,
    id,
    name,
    label,
    error,
    onchange
  }: Props = $props();

  let inputElement: HTMLInputElement;

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    onchange?.(value);
  }

  export function focus() {
    inputElement?.focus();
  }
</script>

<div class="input-group">
  {#if label}
    <label for={id} class="label">
      {label}
      {#if required}<span class="required">*</span>{/if}
    </label>
  {/if}
  
  <input
    bind:this={inputElement}
    {type}
    {id}
    {name}
    {placeholder}
    {disabled}
    {required}
    {value}
    class="input"
    class:error={error}
    oninput={handleInput}
  />
  
  {#if error}
    <span class="error-message">{error}</span>
  {/if}
</div>

<style>
  .input-group {
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

  .input {
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border-color, #d1d5db);
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background: white;
  }

  .input:focus {
    outline: none;
    border-color: var(--primary-color, #ff3e00);
    box-shadow: 0 0 0 3px rgba(255, 62, 0, 0.1);
  }

  .input:disabled {
    background: #f9fafb;
    color: #9ca3af;
    cursor: not-allowed;
  }

  .input.error {
    border-color: #ef4444;
  }

  .input.error:focus {
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
  }

  .error-message {
    font-size: 0.875rem;
    color: #ef4444;
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Input" / "Input.svelte").write_text(input_component)
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Input" / "index.ts").write_text("export { default } from './Input.svelte';")
    
    def _create_modal_component(self) -> None:
        """Create Modal component."""
        modal_component = '''<script lang="ts">
  import { clickOutside } from '$actions';
  import type { Snippet } from 'svelte';

  interface Props {
    open?: boolean;
    onClose?: () => void;
    title?: string;
    children: Snippet;
    footer?: Snippet;
  }

  let { open = false, onClose, title, children, footer }: Props = $props();

  function handleEscape(event: KeyboardEvent) {
    if (event.key === 'Escape' && open) {
      onClose?.();
    }
  }

  function handleClickOutside() {
    onClose?.();
  }
</script>

{#if open}
  <div class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby={title ? 'modal-title' : undefined}>
    <div 
      class="modal-content" 
      use:clickOutside={handleClickOutside}
    >
      <div class="modal-header">
        {#if title}
          <h2 id="modal-title" class="modal-title">{title}</h2>
        {/if}
        <button class="close-button" onclick={onClose} aria-label="Close">
          ✕
        </button>
      </div>
      
      <div class="modal-body">
        {@render children()}
      </div>
      
      {#if footer}
        <div class="modal-footer">
          {@render footer()}
        </div>
      {/if}
    </div>
  </div>
{/if}

<svelte:window onkeydown={handleEscape} />

<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .modal-content {
    background: white;
    border-radius: 8px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    max-width: 32rem;
    width: 100%;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 1.5rem 0;
  }

  .modal-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-color, #333);
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

  .modal-body {
    padding: 1.5rem;
    flex: 1;
    overflow-y: auto;
  }

  .modal-footer {
    padding: 0 1.5rem 1.5rem;
    border-top: 1px solid #e5e7eb;
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
  }
</style>
'''
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Modal" / "Modal.svelte").write_text(modal_component)
        (self.frontend_dir / "src" / "lib" / "components" / "ui" / "Modal" / "index.ts").write_text("export { default } from './Modal.svelte';")