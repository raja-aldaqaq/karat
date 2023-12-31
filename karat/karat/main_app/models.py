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
    user = models.ForeignKey(User , on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'pk' : self.id})
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

karat=((24, '24 k'),(22, '22 k'),(21, '21 k'),(18, '18 k'),(14, '14 k'))

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    karat = models.IntegerField(choices=karat, default=karat[2])
    weight = models.FloatField()
    quantity_available = models.IntegerField()
    image = models.ImageField(upload_to="main_app/static/uploads", default="")
    category = models.CharField(
        max_length=1, choices=categories, default=categories[0][0])
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} from {self.shop}'

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'pk' : self.id})

    class Meta:
        ordering = ['-id']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    


# class User(models.Model):
#     first_name = models.CharField
#     last_name = models.CharField
#     email = models.EmailField

#     def get_absolute_url(self):
#         return reverse('detail', kwargs={'user_id' : self.id})
#     def __str__(self):
#         return f'{self.name}'

    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
        

