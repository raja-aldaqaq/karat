from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from .models import Shop
from django.contrib.auth.decorators import login_required




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

@login_required
def profile(request):
    return render(request, 'users/profile.html')

