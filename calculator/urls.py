from django.urls import path
from . import views

app_name = 'calc'

urlpatterns = [
    path('', views.calculator_page, name='calculator')
]
