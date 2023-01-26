from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

class VisitorTest(FunctionalTest):

    def test_home_page_functionality(self):
        # User visits the page and sees my name and information at the top
        # of the page
        self.browser.get(self.live_server_url + reverse('home'))
        self.assertIn('Chondosha', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Jonathan Miller', header_text)

        # There is a descriptive paragraph with links to github and my resume
        description = self.browser.find_element(By.CSS_SELECTOR, '.description').text
        self.assertIn("This is my description paragraph.", description)

        github_link = self.browser.find_element(By.CSS_SELECTOR, '.github-link').text
        self.assertIn("github", github_link)
        #and resume

        # under my information there are several links to apps and websites
        # I have created
        mini_projects = self.browser.find_element(By.CSS_SELECTOR, '.miniprojects').text
        self.assertIn("ToDo List", mini_projects)

        # at the top of the page is a navigation bar with options
        # home, apps, about, account, logout
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')

        # user clicks on app link and it takes them to an app's page
        self.browser.find_element(By.LINK_TEXT, 'ToDo List').click()
        current_url = self.browser.current_url
        expected_url = self.live_server_url + reverse('todo_home')
        self.assertEqual(current_url, expected_url)

        # app page still has nav bar at the top
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')

        # app functionality will be tested separately

        # user can click home button on navbar to return to home page
        self.browser.find_element(By.LINK_TEXT, 'Home').click()
        current_url = self.browser.current_url
        expected_url = self.live_server_url + reverse('home')
        self.assertEqual(current_url, expected_url)

        self.browser.quit()

        self.fail("Finish test!")
