from django.urls import path
from . import views

# app_name = 'store'

urlpatterns = [
    path('', views.store,name='store'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),

    path('login/', views.user_login,name='user_login'),
    path('logout/', views.user_logout,name='user_logout'),
    path('register/', views.register, name='register'),

    path('cart/', views.cart , name = 'cart'),
    path('checkout/',views.checkout , name = 'checkout'),
    path('update_item/', views.updateItem , name="update_item"),
    path('process_order/', views.processOrder , name="process_order"),
    path('product_display/<int:product_id>/',views.productDisplay, name='product_display'),

    path('product/',views.ProductViewSet.as_view(),name='product'),
    path('product/<pk>/',views.ProductDetail.as_view(),name='product_view'),

    path('order/',views.OrderViewSet.as_view(),name='order'),
    path('order/<pk>/',views.OrderDetailSet.as_view(),name='order_view'),

    path('productimg/',views.ProductImgViewSet.as_view(),name='productimg'),
    path('productimg/<pk>/',views.ProImgSet.as_view(),name='productimg_view'),

    path('orderitem/',views.OrderItemViewSet.as_view(),name='orderitem'),
    path('orderitem/<pk>/',views.OrderItemViewSet.as_view(),name='orderitem_view'),

    path('shipping/',views.ShippingViewSet.as_view(),name='shipping'),
    path('shipping/<pk>/',views.ShippingViewSet.as_view(),name='shipping_detail'),

]
