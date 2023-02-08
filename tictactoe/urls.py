from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('game', views.main_page, name='main_page')
]
