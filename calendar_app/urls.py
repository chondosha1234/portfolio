from django.urls import path
from . import views

app_name = "cal"

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event_details/<int:event_id>/', views.event_details, name='event_details'),
]
