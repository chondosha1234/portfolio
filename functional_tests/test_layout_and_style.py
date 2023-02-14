from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

class LayoutAndStyleTest(FunctionalTest):

    def test_layout_and_style(self):

        # user goes to home page
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.set_window_size(1024, 728)

        # the description paragraph is centered
        description = self.browser.find_element(By.NAME, 'description')
        self.assertAlmostEqual(
            description.location['x'] + description.size['width'] / 2,
            512,
            delta=10
        )
