from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form = SignUpForm()

    return render(request, 'authentication/signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('falselogin')
        elif user is not None:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'authentication/login.html')

def falselogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('falselogin')
        elif user is not None:
            login(request, user)
            return redirect('home')

    else:
        return render(request, 'authentication/falselogin.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def user(request):
    return render(request, 'user.html')