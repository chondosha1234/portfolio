from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import FunctionalTest

class CalculatorTest(FunctionalTest):

    def test_basic_arithmetic_functions(self):

        # user goes to calculator page
        # they see a display, buttons 0-9, decimal, clear, equals, and operators
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Calculator').click()
        self.assertRegex(self.browser.current_url, '/calculator/')

        # they try addition.
        # they press the 1 button
        self.wait_for_element_id('one').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '1')
        # then they press plus button , display still shows 1
        self.wait_for_element_id('add').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '1')
        # then they press 2 button, display shows 2
        self.wait_for_element_id('two').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '2')
        # then they press equals button, and display shows 3
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '3')

        # user hits the clear 'CE' button and hits clear 'AC' button to
        # start over completely
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # user tests clear function.
        # user enters 3 + 3 and then hits 'CE' to clear only the second 3
        self.wait_for_element_id('three').click()
        self.wait_for_element_id('add').click()
        self.wait_for_element_id('three').click()
        self.wait_for_element_id('clear').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '0')
        # then changes it to 5 and presses equals
        self.wait_for_element_id('five').click()
        # the result display is 8
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '8')

        # user hit CE and then AC to all clear
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # next they test subtraction
        # they press 5 button
        self.wait_for_element_id('five').click()
        # then they press substract, display shows 5
        self.wait_for_element_id('subtract').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '5')
        # then they press 2 button, and display shows 2
        self.wait_for_element_id('two').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '2')
        # then they press equals and it shows 3
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '3')

        # users hit clear twice for all clear
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # they similarly test multiplication with 5 x 4 = 20
        self.wait_for_element_id('five').click()
        self.wait_for_element_id('multiply').click()
        self.wait_for_element_id('four').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '20')

        # user all clears
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # they test division with 15 / 5 = 3
        self.wait_for_element_id('one').click()
        self.wait_for_element_id('five').click()
        self.wait_for_element_id('divide').click()
        self.wait_for_element_id('five').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '3')

        # they all clear
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # user wants to test how decimal works
        # first they enter a number 1.5 and add it to 2 to make 3.5
        self.wait_for_element_id('one').click()
        self.wait_for_element_id('decimal').click()
        self.wait_for_element_id('five').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '1.5')

        self.wait_for_element_id('add').click()
        self.wait_for_element_id('two').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '3.5')

        # they all clear it
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # then they press decimal when there is clear display and it shows 0.
        # then they press 5 to make 0.5 and add it to 2 to get 2.5
        self.wait_for_element_id('decimal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '0.')

        self.wait_for_element_id('five').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '0.5')

        self.wait_for_element_id('add').click()
        self.wait_for_element_id('two').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '2.5')


    def test_repeated_equals_and_single_operator(self):

        self.browser.get(self.live_server_url + reverse('calc:calculator'))
        # user enters a basic addition equation 5 + 1
        self.wait_for_element_id('five').click()
        self.wait_for_element_id('add').click()
        self.wait_for_element_id('one').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '6')

        # user hits equals again immediately and the calc adds the second number
        # again as many times as you hit equals. the first time is 7
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '7')
        # and again to make 8
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '8')

        # user all clears display
        self.wait_for_element_id('clear').click()
        self.wait_for_element_id('clear').click()

        # user enters a number and an operator and presses equals
        # the result is the equivalent ->   2 + =  ->  2 + 2 = 4
        self.wait_for_element_id('two').click()
        self.wait_for_element_id('add').click()
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '4')

        # and they press equals again to get 6
        self.wait_for_element_class('key-equal').click()
        display = self.wait_for_element_class('calculator-display').text
        self.assertEqual(display, '6')
