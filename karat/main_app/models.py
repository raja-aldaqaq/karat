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
        return reverse('detail', kwargs={'shop_id' : self.id})
    def __str__(self):
      return f'{self.name}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
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
    description = models.TextField()
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

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'pk' : self.id})

    class Meta:
        ordering = ['-id']


    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'product_id': self.id
        })
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'product_id': self.id
        })

# class OrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.FloatField()
#     item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"
#     def get_total_item_price(self):
#         return self.quantity * self.item.price

# class Order(models.Model):
#     total_amount = models.FloatField()
#     date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     items = models.ManyToManyField(OrderItem)
#     ordered = models.BooleanField(default=False)
#     def __str__(self):
#         return self.user.username
#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_final_price()