from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ToDoListTest(FunctionalTest):

    def test_start_simple_list(self):
        # user goes to home page
        self.browser.get(self.live_server_url)
        # they see a link to a todo list application
        todo_link = self.browser.find_element(By.LINK_TEXT, 'ToDo List')

        # they click the link and are taken to todo list page
        todo_link.click()
        self.assertRegex(self.browser.current_url, '/todo')

        # at the top they see To Do List
        title = self.browser.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('To Do List', title)

        # there are 2 buttons that say current tasks and completed tasks
        self.browser.find_element(By.LINK_TEXT, 'Current Tasks')
        self.browser.find_element(By.LINK_TEXT, 'Completed Tasks')

        # there is an input that says add task
        inputbox = self.browser.find_element(By.ID, "add-item")

        # user enters an item into the add task box  'Buy milk'
        inputbox.send_keys('Buy milk')
        # user presses enter and item appears on list as 1. Buy Milk with a checkbox
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("Buy milk") ####

        # page creates a new url for this list
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/todo/.+')

        # user enters second item 'buy bread'
        inputbox = self.browser.find_element(By.ID, "add-item")
        inputbox.send_keys('Buy bread')
        inputbox.send_keys(Keys.ENTER)

        # page now has 2 entries
        self.wait_for_row_in_table("Buy milk")
        self.wait_for_row_in_table("Buy bread")

        # first user leaves page
        self.browser.quit()

        # user2 visits home page and goes to to-do list and there is no list there
        self.setUp()
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy bread', page_text)
        self.assertNotIn('Buy milk', page_text)

        # user2 enters an item 'buy chocolate'
        inputbox = self.browser.find_element(By.ID, "add-item")
        inputbox.send_keys('Buy chocolate')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("Buy chocolate")

        # page creates new url for the list
        # it is different from user 1
        user2_url = self.browser.current_url
        self.assertRegex(user2_url, '/todo/.+')
        self.assertNotEqual(user2_url, user_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy bread', page_text)
        self.assertIn('Buy milk', page_text)
