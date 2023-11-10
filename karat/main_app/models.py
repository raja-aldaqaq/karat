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
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


