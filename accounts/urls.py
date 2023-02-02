from django.urls import path
from . import views

#app_name = 'accounts'

urlpatterns = [
    path('login', views.login, name='login'),
    path('create_account', views.create_account, name='create_account'),
    path('logout', views.logout, name='logout'),
]
