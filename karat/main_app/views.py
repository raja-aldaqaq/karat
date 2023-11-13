from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shop, Product, Cart, CartItem, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
# Create your views here.


class shopCreate(CreateView):
    model = Shop
    fields = ['name', 'CR', 'Email', 'address', 'phone', 'logo']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class shopUpdate(UpdateView):
    model = Shop
    fields = ['name', 'CR', 'Email', 'address', 'phone', 'logo']


class shopDelete(DeleteView):
    model = Shop
    success_url = '/shops/'


def home(request):
    return render(request, 'index.html')


def shops_index(request):
    # shops=Shop.objects.filter(user = request.user)
    shops = Shop.objects.all()
    print(shops)
    return render(request, 'shops/index.html', {'shops': shops})


def shops_detail(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    return render(request, 'shops/detail.html', {'shop': shop})

    form = UserCreationForm()
    # context =
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login immedietly after signup
            return redirect('index')
        else:
            error_message = 'Invalid Signup - please try again later', form.error_messages

    form = UserCreationForm()
    # context =
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'karat', 'category', 'weight',
              'quantity_available', 'image']  # M to M cannot use all


class ProductList(LoginRequiredMixin, ListView):
    model = Product


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'karat', 'weight', 'quantity_available',
              'image', 'category']  # M to M cannot use all


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/products/'

# CONDITION TO CART //
# 1- ADD TO CART
# 2- Delete from cart
# 3- DECREASE AND INCREASE QUANTITY
# 4- View CART
# 5- When the user clicks add to cart there is total Price function if will get the quantity from cartitem and multiply by the price and + FOr all elements //  Should be changes if the user changed the amount
# 6- CLick plaace order the status will be changed and the cart will be wmpty // delete cart
# Alsoooooooo we have to check the stock !!!
# def Cart(request, user_id, shop_id):
#     Cart.objects.create(user_id=user_id, shop_id=shop_id)


# @login_required
# def add_to_cart(request, product_id, user_id, shop_id):
#     # GET THE PRODUCT INFORMATION
#     product = Product.objects.get(pk=product_id)
#     # cart, created = Cart.objects.get_or_create(user=user_id)
#     cart = Cart.objects.get(user=user_id, ordered=False)
#     # IFFFF CARTTT IS NULLLL
#     if not cart:
#         cart = Cart.objects.create(user=user_id, ordered=False)
#     # IF there is A cart
#     if cart:
#         # CHECKKK IFFF THE SHOP = THE NEW PRODUCT
#         if product.shop == shop_id:
#             cart_item, item_created = CartItem.objects.get_or_create(
#                 cart=cart, product=product_id)
#             if not item_created:
#                 cart_item.quantity = cart_item.quantity + 1
#                 cart_item.save()
#     return render(request, 'shops/index.html')

# Function to get the product id and remove it from cart
# @login_required
# def add_to_cart(request, product_id, user_id, shop_id):
#     product = Product.objects.get(pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=user_id)
#     cart_item, item_created = CartItem.objects.get_or_create(
#         cart=cart, product=product)
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return render(request, 'cart/cart.html')


# @login_required
# def view_cart(request, user_id):
#     try:
#         cart = Cart.objects.get(user_id=user_id)
#         cart_items = CartItem.objects.filter(cart=cart)
#     except:
#         cart = None
#         cart_items = None
#     return render(request, 'cart/cart.html', {'cart_items': cart_items})

# #     try:
#         cart = Cart.objects.get(id=user_id)
#     except Cart.DoesNotExist:
#         cart = None
#     return render(request, 'cart/cart.html', {'cart': cart})

# def get_total_item_price(self):
#     return self.quantity * self.item.price

# def get_total(self):
#     total = 0
#     for order_item in self.items.all():
#         total += order_item.get_final_price()


# @login_required
# def place_order(request, user_id):
#     cart = Cart.objects.get(user_id=user_id)
#     cart.ordered = True
#     # DECREASE THE QUANTITY FOR EACT PRODUCT IN THE ITEM


# @login_required
# def remove_from_cart(request, product_id):
#     # Get the product from Product_id
#     product = Product.objects.get(pk=product_id)
#     # GET the cart by the user id // Retrieve cart created by user
#     cart = Cart.objects.get(user=request.user)
#     try:
#         # Retrieve cart item from the user cart
#         cart_item = cart.objects.get(product_id=product_id)
#         if cart_item.quantity >= 1:
#             cart_item.delete()
#     except CartItem.DoesNotExist:
#         pass

#     return render(request, 'cart/cart.html', {'cart': cart})

# Get the the data in the cart


# IF THE USER CLICKED ON INCRESE

# @login_required
# def increase_cart_item(request, product_id, user_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Cart.objects.get(user_id=user_id)
#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart, product=product)
#     cart_item.quantity += 1
#     cart_item.save()

#     return redirect('cart/cart.html')
# # Decrese the Amount In Cart


# @login_required
# def decrease_cart_item(request, product_id, user_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Cart.objects.get(user_id=user_id)
#     cart_item = cart.objects.get(product_id=product_id)
#     # WRONG AS THE QUANTITY IS IN ORDERITEM ???
#     if cart_item.product.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')

# INCOMPLETE
# increase the size from stock


#     CartItem.objects.get(id=user_id).item.add(product_id)
#     return messages.info("This item quantity was ADDED.")
    # # cart = Cart(request)
    # # ERRROOOORRRR HEREEEE ??????
    # item = get_object_or_404(CartItem, id=product_id)
    # # cart.add(product_id)
    # order_item, created = CartItem.objects.get_or_create(
    #     item=item,
    #     user=request.user,
    #     ordered=False
    # )
    # order_qs = Cart.objects.filter(user=request.user, ordered=False)
    # if order_qs.exists():
    #     order = order_qs[0]
    #     # check if the order item is in the order
    #     if order.items.filter(product_id=product_id).exists():
    #         order_item.quantity += 1
    #         order_item.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return redirect("/")
    #     else:
    #         order.items.add(order_item)
    #         messages.info(request, "This item was added to your cart.")


# def Cart(request, user_id):
#     try:
#         cart = Cart.objects.get(id=user_id)
#     except Cart.DoesNotExist:
#         cart = None
#     return render(request, 'cart/cart.html', {'cart': cart})
