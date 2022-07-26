const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const navMenu2 = document.querySelector(".nav-menu")
const hamburger2 = document.querySelector(".menu-input")

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
}


function toggleNav(e){

    navMenu2.classList.toggle("education-nav", "basis-1/2",)
    navMenu2.classList.toggle("education-nav", "basis-1/2",)
    navMenu2.classList.toggle("hidden")

    console.log(e)
}

hamburger2.addEventListener('click', toggleNav)