from django.urls import path
from . import views
from .views import profile


urlpatterns = [
  path('', views.home, name='home'),
  path('shops/', views.shops_index, name='index'),

  path('shop/create', views.shopCreate.as_view(), name='shop_create'),
  



  #signup
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', profile, name='users-profile'),

]