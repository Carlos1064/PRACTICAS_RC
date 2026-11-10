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
  const showClientError = function (control) {
    const field = control.closest('.form-field');
    if (!field) return;
    let error = field.querySelector('[data-client-error]');
    if (control.validity.valid) {
      control.removeAttribute('aria-invalid');
      if (error) error.remove();
      return;
    }
    control.setAttribute('aria-invalid', 'true');
    if (!error) {
      error = document.createElement('p');
      error.className = 'field-error';
      error.setAttribute('role', 'alert');
      error.dataset.clientError = 'true';
      control.insertAdjacentElement('afterend', error);
    }
    error.textContent = control.validationMessage || 'Revisa este campo.';
  };
  document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      const invalid = Array.from(form.querySelectorAll('input, select, textarea')).filter(function (control) {
        return !control.validity.valid;
      });
      if (invalid.length) {
        event.preventDefault();
        form.classList.add('was-validated');
        invalid.forEach(showClientError);
        invalid[0].focus();
      }
    });
    form.addEventListener('input', function (event) {
      if (event.target.matches('input, select, textarea')) showClientError(event.target);
    });
    form.addEventListener('change', function (event) {
      if (event.target.matches('input, select, textarea')) showClientError(event.target);
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
