from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




# Create your models here.



class Shop(models.Model):
    name = models.CharField(max_length=100)
    CR = models.CharField(max_length=10)
    Email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="main_app/static/uploads", default="")
    user = models.ForeignKey(User , on_delete=models.CASCADE)


    def get_absolute_url(self):
      return reverse('detail', kwargs={'shop_id' : self.id})
    def __str__(self):
      return f'{self.name}'


