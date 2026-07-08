(function () {
  'use strict';

  // ===== Theme toggle =====
  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('taskflow-theme') || 'light';
  html.setAttribute('data-theme', savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('taskflow-theme', next);
    });
  }

  // ===== Footer date =====
  const footerDate = document.getElementById('footerDate');
  if (footerDate) {
    footerDate.textContent = new Date().toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }

  // ===== Toast notifications =====
  const toastContainer = document.getElementById('toastContainer');

  function showToast(message, type) {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast toast--${type || 'info'}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  }

  if (window.__flashMessages) {
    window.__flashMessages.forEach(([type, message]) => {
      showToast(message, type === 'message' ? 'info' : type);
    });
  }

  // ===== Modal handling =====
  document.querySelectorAll('[data-bs-toggle="modal"]').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.getAttribute('data-bs-target');
      const modal = document.querySelector(targetId);
      if (modal) modal.classList.add('show');
    });
  });

  document.querySelectorAll('[data-dismiss="modal"]').forEach((el) => {
    el.addEventListener('click', () => {
      el.closest('.modal')?.classList.remove('show');
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal.show').forEach((m) => m.classList.remove('show'));
    }
  });

  // ===== Task toggle =====
  const csrfToken = window.__csrfToken || '';

  function updateStats(active, completed) {
    const total = active + completed;
    const countEl = document.getElementById('count');
    const statActive = document.getElementById('statActive');
    const statCompleted = document.getElementById('statCompleted');
    const progressFill = document.getElementById('progressFill');
    const progressPercent = document.getElementById('progressPercent');

    if (countEl) countEl.textContent = active;
    if (statActive) statActive.textContent = active;
    if (statCompleted) statCompleted.textContent = completed;

    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    if (progressFill) progressFill.style.width = `${pct}%`;
    if (progressPercent) progressPercent.textContent = `${pct}%`;
  }

  document.querySelectorAll('.task-checkbox input').forEach((checkbox) => {
    checkbox.addEventListener('click', async (e) => {
      e.preventDefault();
      const taskId = checkbox.dataset.taskId;
      const card = checkbox.closest('.task-card');
      const wasChecked = checkbox.checked;

      try {
        const formData = new FormData();
        formData.append('task_id', taskId);
        formData.append('csrf_token', csrfToken);

        const response = await fetch('/toggle', {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });

        if (!response.ok) throw new Error('Toggle failed');

        const data = await response.json();
        checkbox.checked = data.done;
        card?.classList.toggle('task-card--done', data.done);
        updateStats(data.active_count, data.completed_count);
      } catch {
        checkbox.checked = wasChecked;
        showToast('Failed to update task. Please try again.', 'danger');
      }
    });
  });

  // ===== Delete confirmation =====
  document.querySelectorAll('.delete-form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      if (!confirm('Delete this task?')) {
        e.preventDefault();
      }
    });
  });

  // ===== Search debounce =====
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchInput.closest('form')?.submit();
      }, 400);
    });
  }

  // ===== Stagger task card animations =====
  document.querySelectorAll('.task-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 0.04}s`;
  });
})();
