from django.shortcuts import render

# Create your views here.
def calculator_page(request):
    return render(request, 'calculator.html')
