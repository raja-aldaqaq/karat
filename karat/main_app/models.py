from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=100)
    CR = models.IntegerField()
    Email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField()
    logo = models.ImageField(upload_to="main_app/static/uploads", default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'shop_id': self.id})

    def __str__(self):
        return f'{self.name}'


categories = (
    ('R', 'Rings'),
    ('E', 'Earings'),
    ('B', 'Bracelets'),
    ('N', 'Necklaces'),
    ('S', 'Sets'),
    ('A', 'Anklets'),
    ('C', 'Chockers'),
    ('G', 'Bangles'),
)


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    karat = models.IntegerField()
    weight = models.FloatField()
    quantity_available = models.IntegerField()
    image = models.ImageField(upload_to="main_app/static/uploads", default="")
    category = models.CharField(
        max_length=1, choices=categories, default=categories[0][0])
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} from {self.shop}'

# class Cart(models.Model):
#     total_amount = models.FloatField()
#     date_added = models.DateTimeField(auto_now=True , null=True)
#     date_orderd = models.DateTimeField(auto_now=True , null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     is_ordered = models.BooleanField(default=False , null=True)
#     # ONLY THE PRODUCTS INSIDE ORDERITEM
#     products = models.ManyToManyField(Product)

#     def __str__(self):
#         return self.user.username


# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.FloatField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Cart, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False, null=True)
    date_orderd = models.DateTimeField(auto_now=True, null=True)
    date_added = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False, null=True)
    items = models.ManyToManyField(CartItem)
    date_orderd = models.DateTimeField(auto_now=True, null=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([(item.product.price) for item in self.items.all()])
