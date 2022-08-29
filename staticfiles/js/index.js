const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const navMenuEdu = document.querySelector(".nav-menu-edu")
const hamburgerEdu = document.querySelector(".menu-input")



function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
}


function toggleNav(e){
    console.log(e)

    navMenu2Edu.classList.toggle("education-nav", "basis-1/2",)
    navMenu2Edu.classList.toggle("hidden")

    console.log(e)
}


hamburger.addEventListener("click", mobileMenu);
hamburgerEdu.addEventListener('click', toggleNav)