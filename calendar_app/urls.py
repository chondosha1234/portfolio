from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "cal"

urlpatterns = [
    path('', login_required(views.CalendarView.as_view()), name='calendar'),
    path('event_details/<int:event_id>/', views.event_details, name='event_details'),
]
