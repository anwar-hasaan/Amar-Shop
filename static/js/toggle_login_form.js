// toggle login-register from
let login_form = document.getElementById('login-form');
let register_form = document.getElementById('register-form');

let indicator = document.getElementById('indicator');
let login_btn = document.getElementById('login');
let register_btn = document.getElementById('register');

if (register_btn){
    register_btn.addEventListener('click', function(){
        register_form.style.transform = "translateX(0px)";
        login_form.style.transform = "translateX(0px)";
        indicator.style.transform = "translateX(100px)";
        
    })
}
if (login_btn){
    login_btn.addEventListener('click', function(){
        register_form.style.transform = "translateX(300px)";
        login_form.style.transform = "translateX(300px)";
        indicator.style.transform = "translateX(0px)";
    })
}

// show or hide password
function showPass(){
    let password = document.getElementById('login-pass');
    if (password.type === 'password'){
        password.type = 'text';
    }else{
        password.type = 'password';
    }
}