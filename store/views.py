from django.shortcuts import render
from . models import *
import json
import datetime
from django.http import JsonResponse
from .utils import cookieCart,cartData ,guestOrder
from math import ceil

# from django.views.decorators.csrf import csrf_exempt

def store(request):
    products = Product.objects.all()
    Trend = Product.objects.filter(status="T")

    context = {'products':products,'Trend':Trend}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
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

    else:
        customer ,order =guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # if order.shipping == True:
    ShippingAddress.objects.create(
    customer=customer,
    order=order,
    address=data['shipping']['address'],
    city=data['shipping']['city'],
    state=data['shipping']['state'],
    zipcode=data['shipping']['zipcode'],
    )


    return JsonResponse('Payment submitted..', safe=False)



def productDisplay(request,product_id):
    prod = Product.objects.get( id = product_id)
    val = ProductImages.objects.all()
    print(val)
    product_images = prod.productimages_set.all()
    print(product_images)
    # print(product_images)
    # print(product_val.price)
    context ={'product': prod, 'product_images': product_images}
    return render(request, 'store/product_detail.html', context)

