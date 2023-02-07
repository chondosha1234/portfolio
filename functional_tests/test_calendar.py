from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime
import time
import calendar

from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from django.conf import settings
from unittest import skip

from .base import FunctionalTest

User = get_user_model()


class CalendarTest(FunctionalTest):

    def create_pre_authenticated_session(self, email, password):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email, password)
        else:
            session_key = create_pre_authenticated_session(email, password)
        # to set a cookie you need to visit domain
        # 404 pages load quickest
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

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


    def test_calendar_app(self):

        # User starts from homepage and sees list of mini projects
        self.browser.get(self.live_server_url + reverse('home'))
        calendar_link = self.browser.find_element(By.LINK_TEXT, 'Calendar')

        # user clicks link for calendar app
        calendar_link.click()

        # user will be directed to the login page
        self.assertRegex(self.browser.current_url, '/accounts/login')

        #user logins in and sees a blank calendar for current month
        #self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')
        #print(self.browser.get_cookies())
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

    @skip
    def test_create_new_events_and_delete(self):

        # User starts from homepage and sees list of mini projects
        self.browser.get(self.live_server_url + reverse('home'))
        calendar_link = self.browser.find_element(By.LINK_TEXT, 'Calendar')
        # user clicks link for calendar app
        calendar_link.click()

        #user logins in and sees a blank calendar for current month
        self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')

        # user sees button to add event
        add_event = self.browser.find_element(By.LINK_TEXT, 'Add Event')
        # user clicks button
        add_event.click()

        # user sees create new event page
        self.assertRegex(self.browser.current_url, '/calendar/event/create/')

        # at the bottom there is a return button
        return_btn = self.browser.find_element(By.LINK_TEXT, 'Return')
        # user clicks and returns to calendar
        return_btn.click()
        self.assertRegex(self.browser.current_url, '/calendar/')

        # user goes to create event page
        add_event.click()

        # there are 4 fields, add event title, start time, end time, and description
        # user enters info and creates event
        title = self.browser.find_element(By.NAME, 'title')
        start_time = self.browser.find_element(By.NAME, 'start_time')
        end_time = self.browser.find_element(By.NAME, 'end_time')
        description = self.browser.find_element(By.NAME, 'description')
        self.assertEqual(
            title.get_attribute('placeholder'),
            'Enter event title'
        )

        title.send_keys('Test event')
        start_time.send_keys()
        end_time.send_keys()
        description.send_keys('This is a test event')

        # at the bottom there is a submit button
        submit_btn = self.browser.find_element(By.NAME, 'Submit-btn')
        # user clicks submit
        submit_btn.click()
        # user is redirected to calendar and can now see their event title on the day they chose
        self.assertRegex(self.browser.current_url, '/calendar/')
        event_link = self.browser.find_element(By.TEXT_LINK, 'Test')

        # user clicks on event title and is taken to event detail page
        event_link.click()
        self.assertRegex(self.browser.current_url, '/calendar/event/details/$')

        # there is a button to return
        return_btn = self.browser.find_element(By.TEXT_LINK, 'Return')
        # user presses return and is taken to calendar again
        return_btn.click()
        self.assertRegex(self.browser.current_url, '/calendar/')
        # their event is still there
        event_link = self.browser.find_element(By.TEXT_LINK, 'Test')
        # they return to event detail
        event_link.click()

        # event detail page shows title, description, and dates
        title = self.browser.find_element(By.NAME, 'title').text
        start_time = self.browser.find_element(By.NAME, 'start_time')
        end_time = self.browser.find_element(By.NAME, 'end_time')
        description = self.browser.find_element(By.NAME, 'description').text

        self.assertEqual(title, 'Test Event')
        self.assertEqual(description, 'This is a test event')

        # there is a delete button for the event
        delete_btn = self.browser.find_element(By.LINK_TEXT, 'Delete')
        # user presses delete and has an 'are you sure prompt'
        delete_btn.click()

        # user clicks no and nothing happens

        # user clicks delete again and yes to prompt
        # user is redirected to calendar and the event is no longer there
        self.assertRegex(self.browser.current_url, '/calendar/')

    @skip
    def test_event_presistence(self):

        # User starts from homepage and sees list of mini projects and clicks link for calendar
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()

        #user logins in and sees a blank calendar for current month
        self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')

        # user sees button to add event and clicks it
        self.browser.find_element(By.LINK_TEXT, 'Add Event').click()

        # user creates event
        title = self.browser.find_element(By.NAME, 'title')
        start_time = self.browser.find_element(By.NAME, 'start_time')
        end_time = self.browser.find_element(By.NAME, 'end_time')
        description = self.browser.find_element(By.NAME, 'description')

        title.send_keys('Test event')
        start_time.send_keys()
        end_time.send_keys()
        description.send_keys('This is a test event')

        self.browser.find_element(By.NAME, 'Submit-btn').click()

        # user returns to create event page and tries to enter invalid event and cannot

        # user is on calendar page and presses logout and is redirected to login page
        self.assertRegex(self.browser.current_url, '/calendar/')
        logout_btn = self.browser.find_element(By.TEXT_LINK, 'Logout')
        self.assertRegex(self.browser.current_url, '/accounts/login')

        # user logs in again and sees their event
        self.create_pre_authenticated_session('user1234@example.org', 'chondosha5563')
        self.browser.find_element(By.TEXT_LINK, 'Test')

        # user presses home button
        self.browser.find_element(By.LINK_TEXT, 'Home').click()
        self.assertRegex(self.browser.current_url, '/')

        # user clicks calendar app again and is sent directly to their calendar
        self.browser.find_element(By.LINK_TEXT, 'Calendar').click()
        self.assertRegex(self.browser.current_url, '/calendar/')
        self.browser.find_element(By.TEXT_LINK, 'Test')

        # user quits
