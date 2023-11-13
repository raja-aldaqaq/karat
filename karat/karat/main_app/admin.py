from django.contrib import admin
from .models import Shop, Product, Cart, CartItem
from .models import Profile


# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
