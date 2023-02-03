from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from unittest import skip

User = get_user_model()

class LoginViewTest(TestCase):

    def test_renders_login_page(self):
        response = self.client.get('/accounts/login')
        self.assertEquals(response.templates[0].name, 'login.html')
        self.assertTemplateUsed(response, 'login.html')

    def test_failed_login_renders_login_page(self):
        response = self.client.post(
            '/accounts/login',
            data={
                'email': "user1234@example.org",
                'password': "chondosha5563"
            }
        )
        self.assertTemplateUsed(response, 'login.html')

    def test_successful_login_authenticates_user(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        response = self.client.post(
            '/accounts/login',
            data={
                'email': "user1234@example.org",
                'password': "chondosha5563"
            }
        )
        self.assertRedirects(response, '/')
        user_id = response.wsgi_request.user
        self.assertEquals(user, user_id)


class CreateAccountviewTest(TestCase):

    def test_renders_create_account_page(self):
        response = self.client.get('/accounts/create_account')
        self.assertEquals(response.templates[0].name, 'create_account.html')
        self.assertTemplateUsed(response, 'create_account.html')

    #succesful post
    def test_succesful_POST_redirects_to_login_page(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'email': 'user1234@example.org',
                'password': 'chondosha5563',
                'confirm_password': 'chondosha5563'
                }
        )
        self.assertRedirects(response, '/accounts/login')

    def test_failed_post_redirects_to_create_account(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'email': 'user1234@example.org',
                'password': '',
                'confirm_password': ''
                }
        )
        self.assertRedirects(response, '/accounts/create_account')

    def test_fails_if_no_password_given(self):
        self.client.post(
            '/accounts/create_account',
            data={
                'email': 'user1234@example.org',
                'password': '',
                'confirm_password': ''
                }
        )
        self.assertEqual(User.objects.count(), 0)

    def test_POST_saves_new_user(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'email': 'user1234@example.org',
                'password': 'chondosha5563',
                'confirm_password': 'chondosha5563'
                }
        )
        new_user = User.objects.first()
        self.assertEqual(new_user.email, 'user1234@example.org')
