from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class VisitorTest(FunctionalTest):

    def test_home_page_functionality(self):
        # User visits the page and sees my name and information at the top
        # of the page
        self.browser.get(self.live_server_url)
        self.assertIn('Chondosha', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Jonathan Miller', header_text)
        # There is a descriptive paragraph with links to github and my resume

        # under my information there are several links to apps and websites
        # I have created

        # at the top of the page is a navigation bar with options
        # home, apps, about, account, logout

        # user clicks on app link and it takes them to an app's page

        # app page still has nav bar at the top

        # app functionality will be tested separately

        # user can click home button on navbar to return to home page
        self.browser.quit()

        self.fail("Finish test!")
