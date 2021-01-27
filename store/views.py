from django.shortcuts import render
from . models import *
import json
import datetime
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_items':0 ,'get_cart_total':0}
        print("cart views:",cart)
        # cartItems = 

        for i in cart:
            # cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']


            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total':total,
            }

            items.append(item)
    context = {'items':items,'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {'items':items,'order': order}
    return render(request, 'store/checkout.html', context)

# @csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action)

    customer = request.user.customer
    product  = Product.objects.get(id= productId)
    order , created = Order.objects.get_or_create(customer=customer , complete=False)

    orderItem , created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()


    # In order to allow non-dict objects to be serialized set the safe parameter to False.
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)