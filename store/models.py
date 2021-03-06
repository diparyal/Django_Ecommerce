from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    # def __str__(self): 

    #     return self.user.id

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:     
            Customer.objects.create(user=instance)
        # instance.person.save()

class Product(models.Model):
    product_status = (
        ('N',"New"),
        ('T',"Trending"),
        ('X','Excel'),
            )
    category_type = (
        ("Men","Men"),
        ("Women","Women"),
        ("Electronic","Electronic"),
        ("Book","Book"),)

    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=10,choices=category_type,null=True, blank=True)
    # subCategory = models.CharField(max_length=50,null=True, blank=True)
    status = models.CharField(max_length=1,choices= product_status,null=True, blank=True)
    description = models.TextField(null=True,blank = True)
    featured = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # To prevent Error occured due to Not having a Image field
    @property
    def imageURL(self):
        try:
            url = self.featured.url
        except:
            url = ''
        return url

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        print('URL:', url)
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    # total_item = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)
        
    # @property
    # def shipping(self):
    #     shipping = False
    #     orderitems = self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.digital == False:
    #             shipping = True
    #     return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address