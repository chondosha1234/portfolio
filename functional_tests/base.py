from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import os
import time

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def login_user_for_test(self):
        self.browser.get(self.live_server_url + reverse('accounts:create_account'))
        self.browser.find_element(By.NAME, 'email').send_keys("user1234@example.org")
        self.browser.find_element(By.NAME, 'password').send_keys("chondosha5563")
        self.browser.find_element(By.NAME, 'confirm_password').send_keys("chondosha5563")
        self.browser.find_element(By.CSS_SELECTOR, '.btn').click()

        self.browser.get(self.live_server_url + reverse('accounts:login'))
        self.browser.find_element(By.NAME, 'email').send_keys("user1234@example.org")
        self.browser.find_element(By.NAME, 'password').send_keys("chondosha5563")
        self.browser.find_element(By.CSS_SELECTOR, '.btn').click()

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except(AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    @wait
    def wait_for_element_name(self, name):
        return self.browser.find_element(By.NAME, name)

    @wait
    def wait_for_element_link(self, link):
        return self.browser.find_element(By.LINK_TEXT, link)

    @wait
    def wait_for_element_id(self, id):
        return self.browser.find_element(By.ID, id)

    @wait
    def wait_for_row_in_table(self, row_text):
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(row_text, page_text)

    @wait
    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'add-item')

    def add_list_item(self, item_text):
        self.get_item_input_box().send_keys(item_text)
        self.wait_for_element_id('add-btn').send_keys(Keys.ENTER)
        self.wait_for_row_in_table(item_text)
