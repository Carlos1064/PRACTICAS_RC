(function () {
  const toggle = document.querySelector('[data-nav-toggle]');
  const menu = document.querySelector('[data-nav-menu]');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      menu.classList.toggle('is-open', !expanded);
    });
  }
  document.querySelectorAll('[data-dismiss]').forEach(function (button) {
    button.addEventListener('click', function () {
      const alert = button.closest('.alert');
      if (alert) alert.remove();
    });
  });
  document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        form.classList.add('was-validated');
        form.querySelector(':invalid')?.focus();
      }
    });
  });
  document.querySelectorAll('[data-dialog-open]').forEach(function (button) {
    button.addEventListener('click', function () {
      const dialog = document.getElementById(button.dataset.dialogOpen);
      if (dialog && typeof dialog.showModal === 'function') dialog.showModal();
    });
  });
  document.querySelectorAll('[data-dialog-close]').forEach(function (button) {
    button.addEventListener('click', function () {
      button.closest('dialog')?.close();
    });
  });
})();
