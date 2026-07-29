document.querySelectorAll('.nav-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const nav = document.getElementById(button.getAttribute('aria-controls'));
    const isOpen = nav.classList.toggle('open');
    button.setAttribute('aria-expanded', String(isOpen));
  });
});
