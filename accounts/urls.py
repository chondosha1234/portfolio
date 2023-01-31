from django.urls import path
from . import views

#app_name = 'accounts'

urlpatterns = [
    path('login', views.account_login, name='login'),
    path('create_account', views.create_account, name='create_account'),
]
