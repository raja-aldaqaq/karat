from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shop, Product, Profile
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class shopCreate(CreateView):
  model = Shop
  fields = ['name', 'CR', 'Email' ,'address', 'phone' , 'logo']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class shopUpdate(UpdateView):
  model = Shop
  fields = ['name', 'CR', 'Email' ,'address', 'phone' , 'logo']

class shopDelete(DeleteView):
  model = Shop
  success_url = '/shops/'


def home(request):
  return render(request, 'index.html')

def shops_index(request):
  # shops=Shop.objects.filter(user = request.user) 
  shops=Shop.objects.all() 
  print(shops)
  return render(request, 'shops/index.html', {'shops':shops})

def shops_detail(request, shop_id):
  shop = Shop.objects.get(id=shop_id)
  return render(request, 'shops/detail.html', {'shop': shop})

def signup(request):
  error_message=''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user) #login immedietly after signup
      return redirect('index') 
    else :
      error_message= 'Invalid Signup - please try again later' , form.error_messages

  form = UserCreationForm()
  # context = 
  return render (request, 'registration/signup.html' , {'form' : form, 'error_message':error_message})


class ProductCreate(LoginRequiredMixin, CreateView):
  model = Product
  fields = ['name', 'description', 'category','price', 'karat',  'weight', 'quantity_available', 'image']

  def form_valid(self, form):
    user = self.request.user
    shop = Shop.objects.get(user=user)
    form.instance.shop = shop
    return super().form_valid(form)


class ProductList(LoginRequiredMixin, ListView):
  model = Product

class ProductDetail(LoginRequiredMixin, DetailView):
  model = Product

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the current user added the product
        context['is_owner'] = self.object.shop.user == self.request.user
        return context

def my_products(request):
  user = request.user
  shop = Shop.objects.get(user=user)
  products=Product.objects.filter(shop=shop)
  return render(request, 'products/my_products.html', {'products':products})


class ProductUpdate(LoginRequiredMixin, UpdateView):
  model = Product
  fields = ['name', 'description','category','price', 'karat', 'weight','quantity_available', 'image']

class ProductDelete(LoginRequiredMixin, DeleteView):
  model = Product
  success_url = '/products/'

@login_required
def profile(request):
    return render(request, 'registration/profile.html')