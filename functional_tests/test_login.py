from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from .base import FunctionalTest
import time

class LoginTest(FunctionalTest):

    def test_can_login_and_logout(self):

        # User goes to home page and see on the top right corner a link / button
        # that says Log In
        # They press the button and it takes them to a login page
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Login').click()

        # user sees the url has the word login
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/login')

        # There is a field for username/email and password
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        self.assertEqual(
            username.get_attribute('placeholder'),
            'Username'
        )

        # under the fields there is a link to create new account
        # user clicks link for create new account
        # new page has url with create_account in it
        self.browser.find_element(By.LINK_TEXT, 'Create New Account').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/create_account')

        # the page is now for entering new account name and 2 password fields
        self.browser.find_element(By.NAME, 'username')
        self.browser.find_element(By.NAME, 'password')
        self.browser.find_element(By.NAME, 'confirm_password')

        # user sees link under the fields for 'Login' which takes them back to
        # the main login page
        # user clicks link for login and goes back to main login page.
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/login')

        # User returns to create new account and enters information
        self.browser.find_element(By.LINK_TEXT, 'Create New Account').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/create_account')

        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        confirm_pwd = self.browser.find_element(By.NAME, 'confirm_password')
        submit = self.browser.find_element(By.CSS_SELECTOR, '.btn')

        username.send_keys("user1234")
        password.send_keys("password1234")
        confirm_pwd.send_keys("password1234")
        submit.click()

        # User presses submit button and is redirected to Login page
        time.sleep(2)  # need to wait
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/login')

        # user enters new login information and is taken to home page
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        submit = self.browser.find_element(By.CSS_SELECTOR, '.btn')

        username.send_keys("user1234")
        password.send_keys("password1234")
        submit.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))

        # user can now see in the top right corner that they are logged in
        # there is now a 'log out' link / button instead of log in
        logout = self.browser.find_element(By.LINK_TEXT, 'Logout')
        account_info = self.browser.find_element(By.NAME, 'account-info').text
        assertEqual(account_info, "Logged in as")

        # user clicks log out and is redirected to home page
        # where they see 'log in' link again
        logout.click()
        self.assertEqual(self.current_url, reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Login')
