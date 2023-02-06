from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'cal'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('create_event/', views.create_event, name='create_event'),
    path('event_details/<int:event_id>/', views.event_details, name='event_details'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event')
]
