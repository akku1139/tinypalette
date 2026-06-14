import { writable } from 'svelte/store';

export type ToastData = {
  id: string,
  type: 'info' | 'success' | 'warning' | 'error',
  title?: string,
  message: string,
  duration?: number,
};
export const toasts = writable<(ToastData)[]>([]);

export const addToast = (options: Omit<ToastData, 'id'>) => {
  const id = Math.random().toString(36).substring(2, 9);
  toasts.update((all) => [...all, { id, ...options }]);
};

export const removeToast = (id: string) => {
  toasts.update((all) => all.filter((t) => t.id !== id));
};
