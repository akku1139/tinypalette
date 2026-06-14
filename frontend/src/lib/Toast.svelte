<script lang='ts'>
import { onMount } from 'svelte';
import { removeToast, type ToastData } from './toastStore.js';

export let toast: ToastData;

let timeoutId: number;

onMount(() => {
  if (toast.duration && toast.duration > 0) {
    timeoutId = setTimeout(() => {
      removeToast(toast.id);
    }, toast.duration);
  }

  return () => {
    if (timeoutId) clearTimeout(timeoutId);
  };
});
</script>

<div class="toast {toast.type}">
  <div class="toast-content">
    {#if toast.title}
      <div class="toast-title">{toast.title}</div>
    {/if}
    <div class="toast-message">{toast.message}</div>
  </div>

  <button class="close-btn" on:click={() => removeToast(toast.id)} aria-label="Close">
    ✕
  </button>

  {#if toast.duration && toast.duration > 0}
    <div
      class="progress-bar"
      style="animation-duration: {toast.duration}ms;"
    ></div>
  {/if}
</div>

<style>
.toast {
  position: relative;
  width: 320px;
  background-color: #252526;
  color: #cccccc;
  border: 1px solid #454545;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  border-top: none;
  border-bottom: none;
}

.toast.info { border-left: 4px solid #3794ff; }
.toast.success { border-left: 4px solid #89d185; }
.toast.warning { border-left: 4px solid #cca700; }
.toast.error { border-left: 4px solid #f48771; }

.toast-content {
  flex-grow: 1;
  margin-right: 12px;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #ffffff;
  font-size: 14px;
}

.toast-message {
  font-size: 13px;
  line-height: 1.4;
}

.close-btn {
  background: transparent;
  border: none;
  color: #cccccc;
  cursor: pointer;
  font-size: 14px;
  padding: 4px;
  margin: -4px -8px 0 0;
  border-radius: 4px;
  transition: background-color 0.2s, color 0.2s;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background-color: rgba(255, 255, 255, 0.3);
  animation-name: shrink;
  animation-timing-function: linear;
  animation-fill-mode: forwards;
}

@keyframes shrink {
  from { width: 100%; }
  to { width: 0%; }
}
</style>
