from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from accounts.authentication import CustomAuthenticationBackend

User = get_user_model()

class AuthenticateTest(TestCase):

    def test_returns_None_if_no_user(self):
        request = HttpRequest()
        result = CustomAuthenticationBackend().authenticate(request, 'fakeuser', 'chondosha5563')
        self.assertIsNone(result)

    def test_returns_existing_user_with_correct_password(self):
        request = HttpRequest()
        email = "user1234@example.org"
        password = "chondosha5563"
        expected_user = User.objects.create(email=email, password=password)
        expected_user.set_password(expected_user.password)
        expected_user.save()
        user = CustomAuthenticationBackend().authenticate(request, email, password)
        self.assertEqual(expected_user, user)

    def test_returns_None_for_existing_user_but_wrong_password(self):
        request = HttpRequest()
        email = "user1234@example.org"
        password = "chondosha5563"
        User.objects.create(email=email, password=password)
        wrong_password = "wrongpassword"
        user = CustomAuthenticationBackend().authenticate(request, email, wrong_password)
        self.assertIsNone(user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email="user1234@example.org", password="chondosha5563")
        desired_user = User.objects.get(email="user1234@example.org")
        found_user = CustomAuthenticationBackend().get_user('user1234@example.org')
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_email(self):
        self.assertIsNone(CustomAuthenticationBackend().get_user('user1234@example.org'))
