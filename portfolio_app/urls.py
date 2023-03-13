from django.urls import path
from . import views

#app_name = 'portfolio'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact', views.contact_me, name='contact_me'),
    path('about', views.about_me, name='about_me'),
]
