from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shop, Product, Order, OrderItem, User
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


def add_to_cart(request, product_id, user_id):
    OrderItem.objects.get(id=user_id).item.add(product_id)
    return messages.info("This item quantity was ADDED.")
    # # cart = Order(request)
    # # ERRROOOORRRR HEREEEE ??????
    # item = get_object_or_404(OrderItem, id=product_id)
    # # cart.add(product_id)
    # order_item, created = OrderItem.objects.get_or_create(
    #     item=item,
    #     user=request.user,
    #     ordered=False
    # )
    # order_qs = Order.objects.filter(user=request.user, ordered=False)
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


def Cart(request, user_id):
    try:
        cart = Order.objects.get(id=user_id)
    except Order.DoesNotExist:
        cart = None
    return render(request, 'cart/cart.html', {'cart': cart})
