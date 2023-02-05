from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

from calendar_app.utils import Calendar
from calendar_app.models import Event

User = get_user_model()

class CalendarUtilityTest(TestCase):

    def test_formatday_returns_string_with_event(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        d = timezone.now()
        cal = Calendar(d.year, d.month)
        event = Event.objects.create(
            user=user,
            title='Test',
            description='test',
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        events = Event.objects.all() # should be one event on that day
        html_str = cal.formatday(d.day, events)
        self.assertIn('Test', html_str)
        self.assertIn('href="/calendar/event_details/1/"', html_str)

    def test_formatday_returns_string_day(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        cal = Calendar(2023, 6)
        events = Event.objects.all() # should be no events
        html_str = cal.formatday(11, events)
        self.assertIn('<span class="date">11</span>', html_str)

    def test_formatday_returns_empty_td_if_no_day(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        cal = Calendar(2023, 6)
        events = Event.objects.all() # should be no events
        html_str = cal.formatday(None, events)
        self.assertEqual('<td></td>', html_str)

    def test_formatweek_returns_html_tr_string(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        cal = Calendar(2023, 6)
        events = Event.objects.all() # should be no events
        week = cal.monthdays2calendar(cal.year, cal.month)[0]
        html_str = cal.formatweek(week, events)
        self.assertIn('<tr>', html_str)

    def test_formatmonth_returns_html_string_with_table(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        cal = Calendar(2023, 6)
        html_str = cal.formatmonth(user, withyear=True)
        self.assertIn('<table', html_str)
        self.assertIn('</table>', html_str)
