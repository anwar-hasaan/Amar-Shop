// increase cart item quantity
$('.quantity-increase').click(function(){
    let product_id = $(this).attr('product_id').toString()
    let quantity_elm = this.parentNode.parentNode.children[1]
    let sub_total_elm = this.parentNode.parentNode.nextElementSibling;
    $.ajax({
        type: 'GET',
        url: '/increase-cart-item',
        data:{
            product_id: product_id
        },
        success: function(data){
            console.log(data)
            quantity_elm.innerText = data.quantity;
            sub_total_elm.innerHTML = "&#2547; "+ data.sub_total;

            document.getElementById('sub-total').innerHTML = "&#2547; " + data.all_prod_subtotal_cost;
            document.getElementById('total').innerHTML = "&#2547; " + data.all_prod_total_cost;

            document.getElementById('quantity-badge').innerText = data.cart_quantity;
        }
    })
})

// decrease cart item quantity
$('.quantity-decrease').click(function(){
    let product_id = $(this).attr('product_id').toString()
    let quantity_elm = this.parentNode.parentNode.children[1]
    let sub_total_elm = this.parentNode.parentNode.nextElementSibling;
    $.ajax({
        type: 'GET',
        url: '/decrease-cart-item',
        data:{
            product_id: product_id
        },
        success: function(data){
            console.log(data)
            quantity_elm.innerText = data.quantity;
            sub_total_elm.innerHTML = "&#2547; "+ data.sub_total;

            document.getElementById('sub-total').innerHTML = "&#2547; " + data.all_prod_subtotal_cost;
            document.getElementById('total').innerHTML = "&#2547; " + data.all_prod_total_cost;

            document.getElementById('quantity-badge').innerText = data.cart_quantity;
        }
    })
})

// remove item
$('.remove').click(function(){
    let product_id = $(this).attr('product_id').toString()
    let item_row = this.parentNode.parentNode.parentNode.parentNode
    $.ajax({
        type: 'GET',
        url: '/remove-cart-item',
        data:{
            product_id: product_id
        },
        success: function(data){
            console.log(data)
            item_row.remove()
            document.getElementById('sub-total').innerHTML = "&#2547; " + data.all_prod_subtotal_cost;
            document.getElementById('total').innerHTML = "&#2547; " + data.all_prod_total_cost;

            document.getElementById('quantity-badge').innerText = data.cart_quantity;
            // if cart is empty then remove the total price section
            let is_empty = document.getElementById('cart-quantity');
            if (is_empty == null){
                let total_price_sec = document.getElementById('total-price');
                let thead = document.getElementById('temp');
                total_price_sec.remove()
                thead.remove()

                let temp_div = document.createElement('div');
                temp_div.setAttribute('class', 'empty-cart')
                let temp_h3 = document.createElement('h3')
                // give msg is empty
                temp_h3.innerText = "You don't have any products in your cart!";
                temp_div.appendChild(temp_h3)
                document.getElementById('cart-main-container').appendChild(temp_div);
            }
            
        } 
    })
})



// select payment option
function cod(){
    let cod = document.getElementById('after-pay-cod');
    cod.style.display = 'block';

    let nagad = document.getElementById('after-pay-nagad');
    nagad.style.display = 'none';

    let bkash = document.getElementById('after-pay-bkash');
    bkash.style.display = 'none';
}
// onclick bkash
function bkash(){
    let bkash = document.getElementById('after-pay-bkash');
    bkash.style.display = 'block';

    let nagad = document.getElementById('after-pay-nagad');
    nagad.style.display = 'none';

    let cod = document.getElementById('after-pay-cod');
    cod.style.display = 'none';
}
// onclick nagad
function nagad(){
    let nagad = document.getElementById('after-pay-nagad');
    nagad.style.display = 'block';

    let bkash = document.getElementById('after-pay-bkash');
    bkash.style.display = 'none';

    let cod = document.getElementById('after-pay-cod');
    cod.style.display = 'none';
}