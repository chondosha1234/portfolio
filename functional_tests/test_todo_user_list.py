from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse

from .base import FunctionalTest


class UserListTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_under_my_lists(self):

        # user logs in and goes to todo list
        self.login_user_for_test()
        self.browser.get(self.live_server_url)
        todo_link = self.browser.find_element(By.LINK_TEXT, 'ToDo List')
        todo_link.click()

        # user starts a new list
        self.add_list_item('Buy bread')
        self.add_list_item('Buy milk')
        first_list_url = self.browser.current_url

        # they notice a 'My Lists' button and clicks it
        self.wait_for_element_link('My Lists').click()

        # they see their list based on first list item text
        # they click on it and it returns them to their list
        self.wait_for_element_link('Buy bread').click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # user decides to start another list
        self.browser.get(self.live_server_url + reverse('todo:todo_list'))
        self.add_list_item('Do homework')
        second_list_url = self.browser.current_url

        # user goes back to My Lists and now sees 2 lists
        self.wait_for_element_link('My Lists').click()
        self.wait_for_element_link('Buy bread')
        self.wait_for_element_link('Do homework')

        # user logs out and goes back to To Do list page
        self.wait_for_element_link('Log out').click()

        # my lists option is gone
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.LINK_TEXT, 'My Lists')

        # user logs back in and checks my lists and sees their lists still there
        self.login_user_for_test()
        self.browser.get(self.live_server_url + reverse('todo:todo_list'))
        self.wait_for_element_link('My Lists').click()
        self.wait_for_element_link('Buy bread')
        self.wait_for_element_link('Do homework')
