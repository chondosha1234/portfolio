from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime, date
import calendar

from calendar_app.models import Event

# Create your views here.

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = f"month={str(prev_month.year)}-{str(prev_month.month)}"
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = f"month={str(next_month.year)}-{str(next_month.month)}"
    return month


class CalendarView(ListView):
    #login_url = "accounts:login"
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def event_details(request):
    return render(request, 'event_details.html')
