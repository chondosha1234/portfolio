from django.shortcuts import render, redirect

# Create your views here.
def account_login(request):
    if request.POST:
        return redirect('home')
    return render(request, 'login.html')

def create_account(request):
    if request.POST:
        return redirect('login')
    return render(request, 'create_account.html')
