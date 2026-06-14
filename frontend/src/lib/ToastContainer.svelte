<script>
import { toasts } from './toastStore.js';
import Toast from './Toast.svelte';
import { flip } from 'svelte/animate';
import { fade, slide } from 'svelte/transition';
</script>

<div class="toast-container">
  {#each $toasts as toast (toast.id)}
    <div
      animate:flip={{ duration: 300 }}
      transition:slide={{ duration: 300 }}
    >
      <div transition:fade={{ duration: 200 }}>
        <Toast {toast} />
      </div>
    </div>
  {/each}
</div>

<style>
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 9999;
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
}
</style>
