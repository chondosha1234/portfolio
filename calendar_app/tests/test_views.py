from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, date, timedelta
from unittest import skip

from calendar_app.views import get_date, prev_month, next_month

User = get_user_model()

class CalendarViewTest(TestCase):

    def test_renders_calendar_page_when_logged_in(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        user.set_password(user.password)
        user.save()
        response = self.client.post(
            '/accounts/login',
            data={
                'email': "user1234@example.org",
                'password': "chondosha5563"
            }
        )
        response = self.client.get('/calendar/')
        self.assertEquals(response.templates[0].name, 'calendar.html')
        self.assertTemplateUsed(response, 'calendar.html')

    def test_renders_login_page_if_no_user_logged_in(self):
        response = self.client.get('/calendar/')
        self.assertRedirects(response, '/accounts/login?next=/calendar/')

    def test_CalendarView_renders_current_month_on_initial_request(self):
        pass


class CreateEventTest(TestCase):
    pass


class EventDetailsTest(TestCase):
    pass


class DeleteEventTest(TestCase):
    pass


class DateFunctionTest(TestCase):

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
