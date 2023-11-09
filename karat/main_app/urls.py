from django.urls import path
from . import views
from .views import profile


urlpatterns = [
  path('', views.home, name='home'),
  path('shops/', views.shops_index, name='index'),
  path('shops/<int:shop_id>', views.shops_detail, name='detail'),

  path('shop/create', views.shopCreate.as_view(), name='shop_create'),
    path('shops/<int:pk>/update/', views.shopUpdate.as_view(), name='shops_update'),
  path('shops/<int:pk>/delete/', views.shopDelete.as_view(), name='shops_delete'),
  



  #signup
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', profile, name='users-profile'),

]