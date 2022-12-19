// toggle menu button
let menu_items = document.getElementById('menu-items');
let menu_btn = document.getElementById('menu-btn');

menu_items.style.maxHeight = "0px";
menu_btn.addEventListener('click', function(){
    if(menu_items.style.maxHeight == "0px"){
        menu_items.style.maxHeight = "200px"
    }
    else{
        menu_items.style.maxHeight = "0px"
    }
})


// toggle image--product details page
let product_img = document.getElementById('product-img');
let small_img = document.getElementsByClassName('small-img');

for (let index = 0; index < small_img.length; index++) {
    small_img[index].addEventListener('click', function(){
            product_img.src = small_img[index].src;
        })    
}



// back to top btn
let btn = $('#button');
$(window).scroll(function() {
  if ($(window).scrollTop() > 600) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});


// profile page toggle buttons (profile, address, order)
function profile(){
  let profile = document.getElementById('profile-section');
  let address = document.getElementById('address-section');
  let changePass = document.getElementById('change-pass-section');

  changePass.style.display = 'none';
  address.style.display = 'none';
  profile.style.display = 'block';
}

function address(){
  let profile = document.getElementById('profile-section');
  let address = document.getElementById('address-section');
  let changePass = document.getElementById('change-pass-section');

  changePass.style.display = 'none';
  profile.style.display = 'none';
  address.style.display = 'block';
}

function change_pass(){
  let changePass = document.getElementById('change-pass-section');
  let profile = document.getElementById('profile-section');
  let address = document.getElementById('address-section');

  profile.style.display = 'none';
  address.style.display = 'none';
  changePass.style.display = 'block';
}