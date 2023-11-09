from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=100)
    CR = models.IntegerField(max_length=10)
    Email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=100)
    logo = models.ImageField(upload_to="main_app/static/uploads", default="")
    user = models.ForeignKey(User , on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('detail', kwargs={'shop_id' : self.id})
    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=150)

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    karat = models.IntegerField()
    quantity_available = models.IntegerField()
    image = models.ImageField(upload_to="main_app/static/uploads", default="")
    category = models.ForeignKey(Category) 
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} from {self.shop}'

    class Meta:
        ordering = ['-date'] # Date descending