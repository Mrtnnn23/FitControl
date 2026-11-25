document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (event) => {
        if (!window.confirm(form.dataset.confirm)) {
            event.preventDefault();
        }
    });
});

const menuButton = document.querySelector('.mobile-toggle');
const sidebar = document.getElementById('sidebar');

if (menuButton && sidebar) {
    menuButton.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        menuButton.setAttribute('aria-expanded', sidebar.classList.contains('open'));
    });
}
