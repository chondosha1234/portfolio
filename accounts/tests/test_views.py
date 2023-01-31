from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginViewTest(TestCase):

    def test_renders_login_page(self):
        response = self.client.get('/accounts/login')
        self.assertEquals(response.templates[0].name, 'login.html')
        self.assertTemplateUsed(response, 'login.html')


class CreateAccountviewTest(TestCase):

    def test_renders_create_account_page(self):
        response = self.client.get('/accounts/create_account')
        self.assertEquals(response.templates[0].name, 'create_account.html')
        self.assertTemplateUsed(response, 'create_account.html')

    #succesful
    def test_succesful_POST_redirects_to_login_page(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'username': 'user1234',
                'password': 'password1234',
                'confirm_password': 'password1234'
                }
        )
        self.assertRedirects(response, '/accounts/login')
    """
    def test_fails_if_no_password_given(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'username': 'user1234',
                'password': '',
                'confirm_password': ''
                }
        )
        self.assertRedirects(response, '/accounts/create_account')
    """
    def test_failed_post_redirects_to_create_account(self):
        pass

    def test_duplicate_user_fails(self):
        pass

    def test_username_is_long_enough(self):
        pass

    def test_fails_if_password_and_confirm_password_dont_match(self):
        pass

    def test_POST_saves_new_user(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'username': 'user1234',
                'password': 'password1234',
                'confirm_password': 'password1234'
                }
        )
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'user1234')
