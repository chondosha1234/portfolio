from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_has_username_and_password(self):
        user = User(username="user1234", password="password1234")
        user.full_clean()

    def test_username_is_primary_key(self):
        user= User(username="user1234", password="password1234")
        self.assertEqual(user.pk, "user1234")
