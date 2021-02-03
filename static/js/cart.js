console.log('cart.js')
// window.onload = function(){
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var price = this.dataset.price
        console.log('productId:', productId, 'Action:', action)

        document.getElementById("my_cart").innerHTML= quantity

        if (user == 'AnonymousUser'){
            addCookieItem(productId,action,price)
        }else{
            updateUserOrder(productId,action)
        }
})
}
// }

function addCookieItem(productId,action,price){
    console.log("User:",user)

    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
            if (quantity== 0){
                quantity =1
            }else{
                quantity = quantity + 1 }
                document.cookie = "quantity="+ quantity + ";path=/";

            // document.getElementById("my_cart").innerHTML = quantity
        }else{
            console.log("This is",quantity)
            cart[productId]["quantity"] += 1
            // for (i= 0 ; cart.length; i++){
            //     console.log("HEllo"+cart[i])
            // }
            // typeof(getCookie('cart')) Type is string
            // var val= JSON.parse(getCookie('cart'))
            // console.log(Object.values(JSON.parse(value)))

            
            // document.getElementById("my_cart").innerHTML= cart[productId]["quantity"]
            quantity = parseInt(quantity) + 1
            // quantity = quantity + 1
            console.log("quant"+quantity)
            document.cookie = "quantity="+ quantity + ";path=/";
            // document.getElementById("my_cart").innerHTML= quantity
            console.log(cart[productId]["quantity"])
        }
    }

    if (action == 'remove'){
        console.log(cart)
        console.log(cart[`${productId}`.trim()])
        console.log(productId)
        quantity = parseInt(quantity) - 1
        cart[`${productId}`.trim()]["quantity"] -= 1
        document.cookie = "quantity="+ quantity + ";path=/";
        document.getElementById("my_cart").innerHTML= quantity
        // document.getElementById("my_cart").innerHTML= cart[`${productId}`.trim()]["quantity"]
        
        if (cart[`${productId}`.trim()]["quantity"] ==0 ){
            delete cart[`${productId}`.trim()]
            // document.getElementsByClassName(`${productId}`.trim()).remove();
            // [document.getElementsByClassName(`${productId}`get_cart_items.trim())].map(n => n && n.remove());
            // document.getElementById("element-id").outerHTML = "";
            return
            
        }
    
    }

    console.log("quantity:"+quantity)
    console.log("productId:"+productId)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    document.getElementById("my_cart").innerHTML= quantity
    document.getElementById("total_items").innerHTML= quantity
    document.getElementById(`${productId}`.trim()).innerHTML= cart[`${productId}`.trim()]["quantity"]

    
    console.log('Cart:',cart)
}


function updateUserOrder(productId,action) {
    console.log("user is authenticated ")

    var url = '/update_item/'

    // Here data is send through 'POST' request
    // so we need to send csrf token 
    // Normally done through FORM
     // But here we are using JS so add X-CSRFToken
    fetch(url, {
        method : 'POST',
        headers : {'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken },

        // IN fetch API we cannot send object to backend 
        // we need to send object as string
        body: JSON.stringify({'productId':productId,
                            'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data' ,data)
        console.log('finally'+`${data['productId']}`)
        document.getElementById("my_cart").innerHTML= data['login_quantity'];
        document.getElementById("total_items").innerHTML= data['login_quantity']

        if (data['item_quantity'] == 0 ){
            document.getElementsByClassName(`${data['productId']}`.trim()).remove()
        }else{
           document.getElementById(`${data['productId']}`.trim()).innerHTML= data['item_quantity']; 
        }
        
        // location.reload()
    })
}