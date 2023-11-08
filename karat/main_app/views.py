from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.



def home(request):
  return render(request, 'index.html')

def karat(request):
  return render()

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

