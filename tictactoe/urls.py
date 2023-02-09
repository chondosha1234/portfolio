from django.urls import path
from . import views

app_name = 'ttt'

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('game', views.main_page, name='main_page')
]
