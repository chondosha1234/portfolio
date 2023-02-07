from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar

from calendar_app.models import Event
from calendar_app.utils import Calendar
from calendar_app.forms import EventForm


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


class CalendarView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


@login_required(login_url='accounts:login')
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        "event": event,
        "event_id": event_id,
    }
    return render(request, 'event_details.html', context)


@login_required(login_url='accounts:login')
def create_event(request):
    if request.POST:
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            Event.objects.get_or_create(
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time
            )
            return redirect('cal:calendar')

    form = EventForm()
    context = {
        'form': form,
    }
    return render(request, 'create_event.html', context)


@login_required(login_url='accounts:login')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('cal:calendar')
