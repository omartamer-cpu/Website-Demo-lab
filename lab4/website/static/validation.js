// Browser checks give quick feedback. The server repeats the same checks.
document.querySelectorAll('[data-form]').forEach(form => {
  form.addEventListener('submit', event => {
    const errors = {};
    const value = name => form.elements.namedItem(name).value;
    const type = form.dataset.form;
    if (type === 'todo') {
      const title = value('title').trim();
      if (!title) errors.title = 'Title is required';
      else if (Array.from(title).length > 200) errors.title = 'Title is too long';
    } else {
      if (!value('email').trim()) errors.email = 'Email is required';
      if (!value('password')) errors.password = 'Password is required';
      if (type === 'register') {
        if (!value('name').trim()) errors.name = 'Name is required';
        else if (Array.from(value('name').trim()).length > 100) errors.name = 'Name is too long (100 characters at most)';
        if (Array.from(value('email').trim()).length > 255) errors.email = 'Email is too long (255 characters at most)';
        if (new TextEncoder().encode(value('password')).length > 72) errors.password = 'Password is too long (72 UTF-8 bytes at most)';
        if (!value('confirm_password')) errors.confirm_password = 'Confirm password is required';
        else if (value('password') && value('password') !== value('confirm_password')) errors.confirm_password = 'Passwords do not match';
      }
    }
    form.querySelectorAll('[data-error]').forEach(el => { el.textContent = errors[el.dataset.error] || ''; });
    if (Object.keys(errors).length) {
      event.preventDefault();
      form.elements.namedItem(Object.keys(errors)[0]).focus();
    }
  });
});
document.querySelectorAll('[data-delete]').forEach(form => {
  form.addEventListener('submit', event => {
    if (!window.confirm('Are you sure?')) event.preventDefault();
  });
});
