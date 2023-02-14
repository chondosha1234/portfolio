from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest

class DeleteAndUpdateTest(FunctionalTest):

    reset_sequences = True

    def test_update_and_delete_works_on_list_items(self):

        # user goes to to-do list page
        self.browser.get(self.live_server_url)
        todo_link = self.browser.find_element(By.LINK_TEXT, 'ToDo List')
        todo_link.click()

        # user starts a new list with item 'Buy bread'
        self.add_list_item('Buy bread')

        # user sees the update task box under add task
        edit_input_id = self.wait_for_element_id('edit-task-id')
        edit_input_text = self.wait_for_element_id('edit-task-text')
        edit_btn = self.wait_for_element_id('edit-btn')

        # user enters the id number next to task and enters the new task information
        # 'Buy milk'
        edit_input_id.send_keys(1)
        edit_input_text.send_keys('Buy milk')
        edit_btn.click()

        # user sees the task has changed to 'Buy milk'
        self.wait_for_row_in_table('Buy milk')

        # user sees the delete input
        delete_input = self.wait_for_element_id('delete-task')
        delete_btn = self.wait_for_element_id('delete-btn')

        # user enters the same id number and presses enter
        delete_input.send_keys(1)
        delete_btn.send_keys(Keys.ENTER)

        # the task is now gone from the list
        with self.assertRaises(NoSuchElementException):
            self.wait_for_element_name('task-list').text
