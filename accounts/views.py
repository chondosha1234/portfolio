from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def account_login(request):
    if request.POST:
        return redirect('home')
    return render(request, 'login.html')

def create_account(request):
    if request.POST:
        new_user = User.objects.create(username=request.POST['username'])
        return redirect('login')
    return render(request, 'create_account.html')
