from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('shops/', views.shops_index, name='index'),
    path('shops/<int:shop_id>', views.shops_detail, name='detail'),

  path('shop/create', views.shopCreate.as_view(), name='shop_create'),
  



  #signup
  path('accounts/signup/', views.signup, name='signup')
]