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
            console.log("User is not authenticated")
        }else{
            updateUserOrder(productId,action)
        }

})
}
// }

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
        location.reload()
    })
}