from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shop, Product, Profile, categories, Order, OrderItem
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm , AddUser
from django.contrib import messages
from django.contrib.auth.models import User

#API
import requests
import ast


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
  api_key = "goldapi-2estzrloof0srh-io"
  symbol = "XAU"
  curr = "SAR"

  url = f"https://www.goldapi.io/api/{symbol}/{curr}"
  
  headers = {
    "x-access-token": api_key,
    "Content-Type": "application/json"
  }
  
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    gold = ast.literal_eval(response.text)
    gold_prices = {
      "price_gram_24k": gold["price_gram_24k"]/10,
      "price_gram_22k": gold["price_gram_22k"]/10,
      "price_gram_21k": gold["price_gram_21k"]/10,
      "price_gram_18k": gold["price_gram_18k"]/10,

    }
    print(gold)
    return render(request, 'index.html' , {'gold': gold, "gold_prices":gold_prices })
  except requests.exceptions.RequestException as e:
    print("Error:", str(e))
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
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user) #login immedietly after signup
      return redirect('index') 
    else :
      error_message= 'Invalid Signup - please try again later' , form.error_messages

  form = SignUpForm()
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


def category(request):
  return render(request, 'products/categories.html', {'categories':categories})


def category_products(request,category):
  # category = request.category
  for category_c, name in categories:
    if category_c == category:
      category_name = name
      break

  products=Product.objects.filter(category=category)
  return render(request, 'products/products_by_category.html', {'products':products, 'category_name':category_name})

class ProductUpdate(LoginRequiredMixin, UpdateView):
  model = Product
  fields = ['name', 'description','category','price', 'karat', 'weight','quantity_available', 'image']

class ProductDelete(LoginRequiredMixin, DeleteView):
  model = Product
  success_url = '/products/'

@login_required
def profile(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = form.save()(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    # return render(request, 'signup.html', {'form': form})
    return render(request, 'registration/login.html', {'form': form})



def addnewuser(request):
  error_message=''
  if request.method == 'POST':
    form = AddUser(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user) #login immedietly after signup
      return redirect('index') 
  else :
    # error_message= 'Invalid Signup - please try again later' , form.error_messages
    form = AddUser()
  return render(request, 'registration/adduser.html' , {'form' : form, 'error_message':error_message})



@login_required
def add_to_cart(request, product_id):
    print('fdgchjkcfxdghjnbvdfghjbvgfhjnbvcxdfghjmnbvd')
    current_user = request.user
    product = Product.objects.get(id=product_id)

    print('current_user',current_user)
    print('product',product)
    # Check if the product quantity is greater than 0
    if product.quantity_available <= 0:
        messages.warning(request, "Product is out of stock.")
        return redirect('products_index')

        # Check if the user has an order with ordered=False
        # try:
    else:
      cart = Order.objects.filter(user=current_user, ordered=False)
      if len(cart)>0:
        print('cart count',len(cart))
        # Check if the product belongs to the same shop as the items in the cart
        if cart[0].shop.id == product.shop.id:
          add_item(current_user, product)
        else:
          messages.warning(request, "All items in the cart should be from the same shop.")
      else:
        print('no cart',len(cart))

        # except Order.DoesNotExist:
        # If no existing cart, create a new order and add the item

        print('current_user',current_user)
        print('product id',product.id)
        print('product shop id',product.shop.id)
        create_order(current_user, product.shop)
        add_item(current_user, product)

            
        return render(request, 'cart/cart.html', {'cart': OrderItem.objects.filter(order__user=current_user, order__ordered=False)})

    return render(request, 'cart/cart.html', {'cart': OrderItem.objects.filter(order__user=current_user, order__ordered=False)})






# @login_required
def add_item(user, product):
    print('add iteeeemmmmmmmmmmm u',user)
    print('add iteeeemmmmmmmmmmm p',product)
    cart = Order.objects.get(user=user, ordered=False)
    OrderItem.objects.create(order=cart, product=product, quantity=1, price=0)

# @login_required
def create_order(user, shop):
    print("user...........",user)
    print("shop...........",shop)
    existing_order = Order.objects.filter(user=user, shop=shop, ordered=False).first()
    if not existing_order:
        # If no existing order, create a new one
        Order.objects.create(user=user, shop=shop, ordered=False, total_amount=0)
    # Order.objects.create(user=user, shop=shop, ordered=False)


def view_cart(request, user_id):
    try:
        cart_items = OrderItem.objects.filter(
            order__user=user_id, order__ordered=False)
        print(cart_items)
    except:
        cart_items = None
    return render(request, 'cart/cart.html', {'cart_items': cart_items})




    
# @login_required
# def add_to_cart(request, product_id, user_id, shop_id):
#     # GET THE PRODUCT INFORMATION
#     product = Product.objects.get(pk=product_id)
#     # cart, created = Order.objects.get_or_create(user=user_id)
#     cart = Order.objects.get(user=user_id, ordered=False)
#     # IFFFF CARTTT IS NULLLL
#     if not cart:
#         cart = Order.objects.create(user=user_id, ordered=False)
#     # IF there is A cart
#     if cart:
#         # CHECKKK IFFF THE SHOP = THE NEW PRODUCT
#         if product.shop == shop_id:
#             cart_item, item_created = OrderItem.objects.get_or_create(
#                 cart=cart, product=product_id)
#             if not item_created:
#                 cart_item.quantity = cart_item.quantity + 1
#                 cart_item.save()
#     return render(request, 'shops/index.html')

# # Function to get the product id and remove it from cart


# @login_required
# def remove_from_cart(request, product_id):
#     # Get the product from Product_id
#     product = Product.objects.get(pk=product_id)
#     # GET the cart by the user id // Retrieve cart created by user
#     cart = Order.objects.get(user=request.user)
#     try:
#         # Retrieve cart item from the user cart
#         cart_item = cart.objects.get(product_id=product_id)
#         if cart_item.quantity >= 1:
#             cart_item.delete()
#     except OrderItem.DoesNotExist:
#         pass

#     return render(request, 'cart/cart.html', {'cart': cart})

# # Get the the data in the cart


# @login_required
# def view_cart(request, user_id):
#     cart = Order.objects.get(user_id=user_id)
#     cart_items = OrderItem.objects.filter(cart=cart)
#     return render(request, 'cart.html', {'cart_items': cart_items})
# # IF THE USER CLICKED ON INCRESE


# @login_required
# def increase_cart_item(request, product_id, user_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Order.objects.get(user_id=user_id)
#     cart_item, created = OrderItem.objects.get_or_create(
#         cart=cart, product=product)
#     cart_item.quantity += 1
#     cart_item.save()

#     return redirect('cart')
# # Decrese the Amount In Cart


# @login_required
# def decrease_cart_item(request, product_id, user_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Order.objects.get(user_id=user_id)
#     cart_item = cart.objects.get(product_id=product_id)
#     # WRONG AS THE QUANTITY IS IN ORDERITEM ???
#     if cart_item.product.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')

# # INCOMPLETE
# # increase the size from stock


# @login_required
# def place_order(request, user_id):
#     cart = Order.objects.get(user_id=user_id)
#     cart.ordered = True
