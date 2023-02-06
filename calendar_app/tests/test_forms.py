from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime

from calendar_app.forms import EventForm

User = get_user_model()

class EventFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = EventForm()
        self.assertIn('placeholder="Enter event title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_no_title(self):
        form = EventForm(data={
            "title": '',
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "description": 'test'
        })
        self.assertFalse(form.is_valid())

    def test_form_validation_for_no_times(self):
        form = EventForm(data={
            "title": 'Test',
            "start_time": '',
            "end_time": datetime.now(),
            "description": 'test'
        })
        self.assertFalse(form.is_valid())

        form = EventForm(data={
            "title": 'Test',
            "start_time": datetime.now(),
            "end_time": '',
            "description": 'test'
        })
        self.assertFalse(form.is_valid())

    def test_form_validation_for_no_description(self):
        form = EventForm(data={
            "title": 'Test',
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "description": ''
        })
        self.assertTrue(form.is_valid())  # no description is ok
