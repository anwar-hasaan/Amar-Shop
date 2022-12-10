// toggle login-register from
let login_form = document.getElementById('login-form');
let register_form = document.getElementById('register-form');

let indicator = document.getElementById('indicator');
let login_btn = document.getElementById('login');
let register_btn = document.getElementById('register');

register_btn.addEventListener('click', function(){
    register_form.style.transform = "translateX(0px)";
    login_form.style.transform = "translateX(0px)";
    indicator.style.transform = "translateX(100px)";
    
})
login_btn.addEventListener('click', function(){
    register_form.style.transform = "translateX(300px)";
    login_form.style.transform = "translateX(300px)";
    indicator.style.transform = "translateX(0px)";
})