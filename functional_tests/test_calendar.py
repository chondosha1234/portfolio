from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, date
import time
import calendar

from unittest import skip
from calendar_app.models import Event

from .base import FunctionalTest

User = get_user_model()


class CalendarTest(FunctionalTest):


    def test_calendar_app(self):

        # User starts from homepage and sees list of mini projects
        self.browser.get(self.live_server_url + reverse('home'))
        calendar_link = self.browser.find_element(By.LINK_TEXT, 'Calendar')

        # user clicks link for calendar app
        calendar_link.click()

        # user will be directed to the login page
        self.assertRegex(self.browser.current_url, '/accounts/login')

        #user logins in and sees a blank calendar for current month
        self.login_user_for_test()

        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()
        self.assertRegex(self.browser.current_url, '/calendar/')

        calendar_table = self.browser.find_element(By.CLASS_NAME, 'calendar')
        calendar_month = self.browser.find_element(By.CLASS_NAME, 'month').text
        month = datetime.now().month
        current_month = f'{calendar.month_name[month]} {datetime.now().year}'
        self.assertEqual(calendar_month, current_month)

        # user sees previous and next buttons
        prev = self.browser.find_element(By.LINK_TEXT, 'Previous Month')
        next = self.browser.find_element(By.LINK_TEXT, 'Next Month')

        # user clicks next and sees the next month
        next.click()
        calendar_month = self.browser.find_element(By.CLASS_NAME, 'month').text
        month = datetime.now().month + 1
        if month > 12:
            month = 1
        next_month = f'{calendar.month_name[month]} {datetime.now().year}'
        self.assertEqual(calendar_month, next_month)

        # they click previous and see the current month
        self.browser.find_element(By.LINK_TEXT, 'Previous Month').click()
        calendar_month = self.browser.find_element(By.CLASS_NAME, 'month').text
        month = datetime.now().month
        current_month = f'{calendar.month_name[month]} {datetime.now().year}'
        self.assertEqual(calendar_month, current_month)

        # user clicks previous again and sees previous month
        self.browser.find_element(By.LINK_TEXT, 'Previous Month').click()
        calendar_month = self.browser.find_element(By.CLASS_NAME, 'month').text
        month = datetime.now().month - 1
        if month < 1:
            month = 12
        prev_month = f'{calendar.month_name[month]} {datetime.now().year}'
        self.assertEqual(calendar_month, prev_month)

        # user clicks next and sees current month
        self.browser.find_element(By.LINK_TEXT, 'Next Month').click()
        calendar_month = self.browser.find_element(By.CLASS_NAME, 'month').text
        month = datetime.now().month
        current_month = f'{calendar.month_name[month]} {datetime.now().year}'
        self.assertEqual(calendar_month, current_month)


    def test_create_new_events_and_delete(self):

        # User starts from homepage and sees list of mini projects
        self.browser.get(self.live_server_url + reverse('home'))

        #user logins in and sees a blank calendar for current month
        self.login_user_for_test()

        calendar_link = self.browser.find_element(By.LINK_TEXT, 'Calendar')
        # user clicks link for calendar app
        calendar_link.click()

        #self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')

        # user sees button to add event and clicks button
        add_btn = self.wait_for_element_link('Add Event')
        add_btn.send_keys(Keys.ENTER)

        # user sees create new event page
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/calendar/create_event/')

        # at the bottom there is a return button
        return_btn = self.browser.find_element(By.LINK_TEXT, 'Return')
        # user clicks and returns to calendar
        return_btn.click()
        self.assertRegex(self.browser.current_url, '/calendar/')

        # user goes to create event page
        add_btn = self.wait_for_element_link('Add Event')
        add_btn.send_keys(Keys.ENTER)

        # there are 4 fields, add event title, start time, end time, and description
        # user enters info and creates event
        title = self.wait_for_element_name('title')
        start_time = self.wait_for_element_name('start_time')
        end_time = self.wait_for_element_name('end_time')
        description = self.wait_for_element_name('description')
        self.assertEqual(
            title.get_attribute('placeholder'),
            'Enter event title'
        )

        d = datetime.now().strftime("%Y-%-m-%-d %H:%M:%S")
        title.send_keys('Test event')
        start_time.send_keys(d)
        end_time.send_keys(d)
        description.send_keys('This is a test event')

        # at the bottom there is a submit button
        submit_btn = self.browser.find_element(By.NAME, 'submit-btn')
        # user clicks submit
        submit_btn.click()

        # user is redirected to calendar and can now see their event title on the day they chose
        self.assertRegex(self.browser.current_url, '/calendar/')
        event_link = self.browser.find_element(By.LINK_TEXT, 'Test event')

        # user clicks on event title and is taken to event detail page
        event_link.click()
        self.assertRegex(self.browser.current_url, '/calendar/event_details/')

        # there is a button to return
        return_btn = self.browser.find_element(By.LINK_TEXT, 'Return')
        # user presses return and is taken to calendar again
        return_btn.click()
        self.assertRegex(self.browser.current_url, '/calendar/')
        # their event is still there
        event_link = self.browser.find_element(By.LINK_TEXT, 'Test event')
        # they return to event detail
        event_link.click()

        # event detail page shows title, description, and dates
        title = self.browser.find_element(By.NAME, 'title').text
        times = self.browser.find_element(By.NAME, 'start_end_times')
        description = self.browser.find_element(By.NAME, 'description').text

        self.assertEqual(title, 'Test event')
        self.assertEqual(description, 'This is a test event')

        # there is a delete button for the event
        delete_btn = self.browser.find_element(By.LINK_TEXT, 'Delete')
        # user presses delete and has an 'are you sure prompt'
        delete_btn.click()

        # user clicks no and nothing happens

        # user clicks delete again and yes to prompt
        # user is redirected to calendar and the event is no longer there
        self.assertRegex(self.browser.current_url, '/calendar/')


    def test_event_presistence(self):

        # User starts from homepage and sees list of mini projects and clicks link for calendar
        self.browser.get(self.live_server_url + reverse('home'))
        self.login_user_for_test()
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()

        # user sees button to add event and clicks it
        add_btn = self.wait_for_element_link('Add Event')
        add_btn.send_keys(Keys.ENTER)

        # user creates event
        title = self.wait_for_element_name('title')
        start_time = self.wait_for_element_name('start_time')
        end_time = self.wait_for_element_name('end_time')
        description = self.wait_for_element_name('description')

        d = datetime.now().strftime("%Y-%-m-%-d %H:%M:%S")
        title.send_keys('Test event')
        start_time.send_keys(d)
        end_time.send_keys(d)
        description.send_keys('This is a test event')

        self.browser.find_element(By.NAME, 'submit-btn').click()

        # user returns to create event page and tries to enter invalid event and cannot

        # user is on calendar page and presses logout and is redirected to login page
        self.assertRegex(self.browser.current_url, '/calendar/')
        self.wait_for_element_class('navbar-toggler').click()
        logout_btn = self.wait_for_element_link('Log out')
        logout_btn.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))

        # user logs in again and sees their event
        #self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')
        self.login_user_for_test()
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()
        self.browser.find_element(By.LINK_TEXT, 'Test event')

        # user presses home button
        self.browser.find_element(By.LINK_TEXT, 'Home').click()
        self.assertRegex(self.browser.current_url, '/')

        # user clicks calendar app again and is sent directly to their calendar
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()
        self.assertRegex(self.browser.current_url, '/calendar/')
        self.browser.find_element(By.LINK_TEXT, 'Test event')

        # user quits
