from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Shop, Product, Profile, categories, Order, OrderItem,User
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm , AddUser
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from datetime import datetime
from django.utils import timezone



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

class shopDetail(DetailView):
  model = Shop


def home(request):
  # api_key = "goldapi-is93rloyil90l-io"
  api_key = "goldapi-is93rloyil90l-i"
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

def my_shopdetail(request):
  user = request.user
  shop = Shop.objects.get(user=user)
  return render(request, 'shops/my_shopdetail.html', {'shop': shop})

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
    return render(request, 'registration/profile.html', {'form': form})



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

class userUpdate(LoginRequiredMixin, UpdateView):
  model = User
  fields = ['username', 'first_name', 'last_name', 'email']
  success_url = '/profile/'




@login_required
def users_detail(request, user_id):
  user = User.objects.get(id=user_id)
  return render(request, 'users/profile.html', {'user': user})




class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('/index/')




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

            
        return redirect('view_cart', user_id=current_user.id)

    return redirect('view_cart', user_id=current_user.id)






@login_required
def add_item(user, product):
    # print('add iteeeemmmmmmmmmmm u',user)
    # print('add iteeeemmmmmmmmmmm p',product)
    cart = Order.objects.get(user=user, ordered=False)
    OrderItem.objects.create(order=cart, product=product, quantity=1, price=0)

@login_required
def create_order(user, shop):
    # print("user...........",user)
    # print("shop...........",shop)
    existing_order = Order.objects.filter(user=user, shop=shop, ordered=False).first()
    if not existing_order:
        # If no existing order, create a new one
        Order.objects.create(user=user, shop=shop, ordered=False, total_amount=0)
    # Order.objects.create(user=user, shop=shop, ordered=False)


def view_cart(request, user_id):
    try:
        cart_items = OrderItem.objects.filter(
            order__user=user_id, order__ordered=False)
        # print(cart_items)
        # for item in cart_items:
        items_context =[]
        item_amout=0
        qty = OrderItem.objects.filter(order_id=cart_items[0].order_id).values('product_id').annotate(quantity=Count('product_id'))
        for q in qty:
          product = Product.objects.get(id=q['product_id'])
          # print('opppppppp:', product)
          # print(q['quantity'])
          # print('price .............',product.price)
          item_amout = q['quantity']*product.price
          print('item_amout',item_amout)
          items_context.append ({
            'product':product,
            'qty':q, 
            'item_amout': item_amout  
          })
        
        # print('qty..........',qty)
    except:
        cart_items = None
    # return render(request, 'cart/cart.html', {'cart_items': cart_items, 'qty':qty})
    return render(request, 'cart/cart.html', {'items_context': items_context, 'qty':qty, 'item_amout':item_amout, 'order_id':cart_items[0].order_id} )


def increase_quantity(request, product_id):
  current_user = request.user
  print('iddddddddddd:',product_id)
  # item_id= OrderItem.objects.get(product_id=product_id).id
  # print('item_id',item_id)
  product_to_add = Product.objects.get(id=product_id)
  print('product_to_add',product_to_add)
  add_item(current_user, product_to_add)
  return redirect('view_cart', user_id= current_user.id)

def decrease_quantity(request, product_id):
  current_user = request.user
  print('product_id:',product_id)
  item_to_delete= OrderItem.objects.filter(product_id=product_id).first()
  item_to_delete.delete()
  return redirect('view_cart', user_id= current_user.id)



def place_order(request, order_id):
  order = Order.objects.get(id=order_id, ordered=False)
  order_items = OrderItem.objects.filter(order=order)

  for order_item in order_items:
    product_price = order_item.product.price
    order_item.price = product_price
    order_item.save()

  total_amount = sum(order_item.price for order_item in order_items)

  # Update the order
  order.total_amount = total_amount
  order.date = datetime.now().date()
  order.ordered = True
  order.save()

  return redirect('order_detail', order_id=order_id)

# # FOR FUTURE :)
# # update the quantity available 
#   for order_item in order_items:
#     product = order_item.product
#     product.quantity_available -= order_item.quantity
#     product.save()

class OrderDetail(LoginRequiredMixin, DetailView):
  model = Order



