from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from calendar_app.models import Event

User = get_user_model()

class EventModelTest(TestCase):

    def test_event_is_connected_to_user(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        event = Event.objects.create(
            user=user,
            title='Test',
            description='test',
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.assertEqual(user, event.user)

    def test_get_absolute_url(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        event = Event.objects.create(
            user=user,
            title='Test',
            description='test',
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.get_absolute_url(), '/calendar/event_details/1/')
