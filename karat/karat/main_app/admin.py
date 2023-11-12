from django.contrib import admin
from .models import Shop, Product
from .models import Profile


# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Profile)


