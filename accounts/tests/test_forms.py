from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class SignUpFormTest(TestCase):
    """
    def test_form_input_has_placeholder_and_css_class(self):
        form = SignUpForm()
        self.assertIn('placeholder="Username"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_username(self):
        form = SignUpForm(data={'username': ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], "Must enter a username")
   """
