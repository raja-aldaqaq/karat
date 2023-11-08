from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('karat/', views.karat, name='karat'),



  #signup
  path('accounts/signup/', views.signup, name='signup')
]