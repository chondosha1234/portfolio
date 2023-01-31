from django.test import TestCase

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
    def test_succesful_post_redirects_to_login_page(self):
        response = self.client.post(
            '/accounts/create_account',
            data={
                'username': 'user1234',
                'password': 'password1234',
                'confirm_password': 'password1234'
                }
        )
        self.assertRedirects(response, '/accounts/login')

    def test_failed_post_redirects_to_create_account(self):
        pass
