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
})();
