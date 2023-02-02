from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

User = get_user_model()

def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def create_account(request):
    if request.POST:
        if not request.POST['password'] or not request.POST['confirm_password']:
            return redirect('create_account')
        else:
            new_user = User.objects.create(email=request.POST['email'], password=request.POST['password'])
            return redirect('login')
    return render(request, 'create_account.html')
