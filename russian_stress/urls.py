from django.urls import path
from . import views

app_name = 'russian'

urlpatterns = [
    path('', views.change_text, name="change_text")
]
