from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
import time

from .base import FunctionalTest

class RussianStressAdderTest(FunctionalTest):

    def test_adds_stress_to_russian_words(self):

        # user goes to home page and see link for russian stress adder app
        # user clicks button and sees page with explanation of russian stress app
        self.browser.get(self.live_server_url)
        russian_link = self.wait_for_element_link("Russian Stress")
        russian_link.click()
        self.assertRegex(self.browser.current_url, '/russian_stress')

        description = self.wait_for_element_class("description-text")
        self.assertIn('Russian Pronunciation Stress Adder', description.text)

        # under the explanation is a text area and button
        submit_btn = self.wait_for_element_id('text-submit')
        text_form = self.wait_for_element_id('id_text')

        # user enters a sentence in russian and presses button
        text_form.send_keys("В Москве состоялись переговоры между лидерами России и Китая.")
        submit_btn.click()

        # user sees "loading..." message appear while it waits to translate sentence
        self.wait_for_element_id('loading')
        time.sleep(10)
        generated_text = self.wait_for_element_class('russian-text').text

        # the sentence appears under the button now with the appropriate stress markings on the words
        self.assertIn("В Москве́ состоя́лись перегово́ры ме́жду ли́дерами Росси́и и Китая.", generated_text)
