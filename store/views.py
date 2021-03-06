from django.shortcuts import render,redirect
from . models import *
from . serializers import *
import json
import datetime
from django.http import JsonResponse
from .utils import cookieCart,cartData ,guestOrder
from rest_framework import generics
import requests
from .forms import UserForm,loginForm

from django import forms
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView
from django.db.models import Q # new

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.core.mail import EmailMessage

# from django.contrib.auth.forms import UserCreationForm
# from django.views.decorators.csrf import csrf_exempt



def store(request):
    # product_val = requests.get('http://127.0.0.1:8000/product/').json()
    # print(product_val)
    # product_trend = [item for item in product_val if item['status']=='T']
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    Trend = Product.objects.filter(status="T")
    # products = product_val
    # Trend = product_trend

    category = Product.objects.values_list('category', flat=True)

    all_category_product = {}
    for cat in category:
        all_category_product[cat] = Product.objects.filter(category=cat)

    # print(all_category_product)


    context = {'products':products,'Trend':Trend,'cartItems':cartItems,'UserForm':UserForm(),'all_category_product':all_category_product}
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
    # print(productId,action)

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

    # return redirect('store')

    # print("orderItem",orderItem)
    # print("orderItem",orderItem.quantity )

 
    # In order to allow non-dict objects to be serialized set the safe parameter to False.
    # return JsonResponse('Item was added',safe=False)
    return JsonResponse({ 'login_quantity':order.get_cart_items,'item_quantity':orderItem.quantity,"productId":productId })

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        #Delete User Order After Checkout
        customer = request.user.customer
        order = Order.objects.get(customer=customer )
        orderItem = OrderItem.objects.filter(order=order).delete()


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


def user_login(request):
    if request.method == 'POST':
        print("logIN value:",request.POST)
        username = request.POST['username']
        password = request.POST['password']
        
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        login(request, user)
        if user:
            return redirect('store')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('store')    
    # else:
    #     form = UserForm()
    #     context = {'form' : form}
    #     return render(request, 'YOUR_APP/register.html', context)


def user_logout(request):
    logout(request)
    return redirect("store")


def SendMail(request):    
    email = EmailMessage('Your Order is Received', 'Thank you for you Order', to=['diparyal22@gmail.com'])
    email.send()
    return redirect("store")



# class SearchResultsView(ListView):
#     model = City
#     template_name = 'search_results.html'
#     queryset = City.objects.filter(name__icontains='Boston') # new


class SearchResultsView(ListView):
    model = Product
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('user_search')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list


class ProductSearch(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Product.objects.all()
        # To Send Search Request: url/?val=
        username = self.request.query_params.get('val', None)
        print(username)
        if username is not None:
            queryset = queryset.filter(id=username)
        return queryset



class OrderSearch(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # login_url = '/login/'

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        customer = self.request.user.customer
        print("customer",customer)
        queryset = Order.objects.filter(customer=customer)
        # value = self.request.query_params.get('val', None)
        print(queryset)
        
        if len(queryset) == 0 :
            queryset = Order.objects.create(customer=customer, complete=False)
            return queryset
            
        return queryset

class OrderItemSearch(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):

        # value = self.request.query_params.get('val', None)
        
        value = self.request.query_params.get('val', None)
        queryset = OrderItem.objects.filter(order=value)
        return queryset

# class ProductSearch(generics.ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         """
#         This view should return a list of all the purchases for
#         the user as determined by the username portion of the URL.
#         """
#         pro_id = self.kwargs['pro_id']
#         return Product.objects.filter(product__id=pro_id)

# class ProductSearch(generics.ListAPIView):
#     search_fields = ['=id']
#     filter_backends = (filters.SearchFilter,)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id']


class ProductViewSet(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductImgViewSet(generics.ListCreateAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImgSerializer

class ProImgSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImgSerializer


class OrderItemViewSet(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ShippingViewSet(generics.ListCreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingSerializer



