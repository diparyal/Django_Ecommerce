console.log('hello')
// window.onload = function(){
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log("User:",user)

        if (user == 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }

})
}
// }

function addCookieItem(productId,action){
    console.log('User is not authenticated')

    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
            // document.getElementById("my_cart").innerHTML =1
        }else{
            console.log("This is",cart)
            cart[productId]["quantity"] += 1
            // document.getElementById("my_cart").innerHTML= cart[productId]["quantity"]
            console.log(cart[productId])
            console.log(cart[productId]["quantity"])
        }
    }

    if (action == 'remove'){
        console.log(cart)
        console.log(cart[productId])
        cart[productId]['quantity'] -= 1
        document.getElementById("my_cart").innerHTML= cart[productId]["quantity"]
        
        if (cart[productId]["quantity"] <=0 ){
            delete cart[productId]
        }
    
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
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
        // location.reload()
    })
}