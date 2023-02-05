from django.test import TestCase
from datetime import datetime
from django.contrib.auth import get_user_model

from calendar_app.utils import Calendar

User = get_user_model()

class CalendarUtilityTest(TestCase):

    def test_formatday_returns_string_with_event(self):
        pass

    def test_formatday_returns_string_day(self):
        pass

    def test_formatday_returns_string_without_day_for_empty_calendar_spot(self):
        pass

    def test_formatweek_returns_html_string(self):
        pass

    def test_formatmonth_returns_html_string_with_table(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        cal = Calendar(2023, 6)
        html_str = cal.formatmonth(user, withyear=True)
        self.assertIn('<table', html_str)
        self.assertIn('</table>', html_str)
