const navbar = document.querySelector('.navbar');
const navbarItems = document.querySelectorAll('.nav-item');

window.onscroll = () => {
    if (window.scrollY > 250) {
        navbar.classList.add('scrolled');
        navbarItems.forEach(item => {
            item.classList.add('scrolled');
        })
    }
    else {
        navbar.classList.remove('scrolled');
        navbarItems.forEach(item => {
            item.classList.remove('scrolled');
        })
    }
};