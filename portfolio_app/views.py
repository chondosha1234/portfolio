from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def about_me(request):
    return render(request, 'home.html')

def contact_me(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'New message from {email}',
                message,
                email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return render(request, 'contact_success.html')

    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)
