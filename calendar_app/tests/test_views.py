from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.utils import timezone
from unittest import skip
import calendar

from calendar_app.models import Event
from calendar_app.forms import EventForm
from calendar_app.views import get_date, prev_month, next_month

User = get_user_model()


class CalendarViewTest(TestCase):

    def test_renders_calendar_page_when_logged_in(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.get('/calendar/')
        self.assertEquals(response.templates[0].name, 'calendar.html')
        self.assertTemplateUsed(response, 'calendar.html')

    def test_renders_login_page_if_no_user_logged_in(self):
        response = self.client.get('/calendar/')
        self.assertRedirects(response, '/accounts/login?next=/calendar/')

    def test_CalendarView_renders_current_month_on_initial_request(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.get('/calendar/')
        today = datetime.today()
        month = calendar.month_name[today.month]
        self.assertContains(response, month)


class CreateEventTest(TestCase):

    def test_renders_create_event_page(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.get('/calendar/create_event/')
        self.assertEquals(response.templates[0].name, 'create_event.html')
        self.assertTemplateUsed(response, 'create_event.html')

    def test_displays_create_event_form(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.get('/calendar/create_event/')
        self.assertIsInstance(response.context['form'], EventForm)

    def test_POST_creates_and_saves_new_event(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.post('/calendar/create_event/', data={
            "title": 'Test',
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "description": 'test'
        })
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.title, 'Test')

    def test_POST_redirects_to_calendar_page(self):
        self.client.force_login(
            User.objects.get_or_create(email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.post('/calendar/create_event/', data={
            "title": 'Test',
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "description": 'test'
        })
        self.assertRedirects(response, '/calendar/')


class EventDetailsTest(TestCase):
    pass


class DeleteEventTest(TestCase):

    def test_delete_removes_event_from_database(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        event = Event.objects.create(
            user=user,
            title='Test',
            description='test',
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.assertEqual(Event.objects.count(), 1)
        self.client.force_login(user)
        response = self.client.get("/calendar/delete_event/1/")
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_redirects_to_calendar(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        event = Event.objects.create(
            user=user,
            title='Test',
            description='test',
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.client.force_login(user)
        response = self.client.get("/calendar/delete_event/1/")
        self.assertRedirects(response, '/calendar/')


class DateFunctionsTest(TestCase):

    def test_get_date_helper_returns_requested_day(self):
        expected_day = date(2023, 6, 1)
        day = get_date('2023-06')
        self.assertEqual(expected_day, day)

    def test_get_date_returns_today_without_request_date(self):
        expected_day = datetime.today().replace(microsecond=0)
        day = get_date('').replace(microsecond=0)
        self.assertEqual(expected_day, day)

    def test_prev_month_returns_previous_month(self):
        expected_month = 'month=2023-5'
        month = prev_month(date(2023, 6, 11))
        self.assertEqual(expected_month, month)

    def test_next_month_returns_next_month(self):
        expected_month = 'month=2023-7'
        month = next_month(date(2023, 6, 11))
        self.assertEqual(expected_month, month)
