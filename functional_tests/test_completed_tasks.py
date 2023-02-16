from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

from .base import FunctionalTest


class CompletedTasksTest(FunctionalTest):

    reset_sequences = True

    def test_completed_tasks_appear_and_disappear(self):

        # user goes to make a new to-do list
        # they enter an item 'Buy bread'
        self.browser.get(self.live_server_url)
        todo_link = self.browser.find_element(By.LINK_TEXT, 'ToDo List')
        todo_link.click()
        self.add_list_item('Buy bread')

        # they see button now that says 'completed tasks'
        completed_btn = self.wait_for_element_link('Completed Tasks')
        completed_btn.click()

        # they press the button and see a blank page
        task_list = self.wait_for_element_class('task-list').text
        self.assertNotIn('Buy bread', task_list)

        # they see button that says 'current tasks'
        current_btn = self.wait_for_element_link('Current Tasks')
        current_btn.click()

        # they press this button and see their list there
        self.wait_for_row_in_table('Buy bread')

        # user clicks the check box next to 'buy bread'
        checkbox = self.wait_for_element_class('checkbox-btn')
        checkbox.click()

        # user goes back to 'completed tasks' and now sees 'buy bread' there
        completed_btn = self.wait_for_element_link('Completed Tasks')
        completed_btn.click()
        task_list = self.wait_for_element_class('task-list').text
        self.assertIn('Buy bread', task_list)

        # they return to list page and uncheck the box
        # when they return to 'completed tasks' page the item is gone
        current_btn = self.wait_for_element_link('Current Tasks')
        current_btn.click()

        checkbox = self.wait_for_element_class('checkbox-btn')
        checkbox.click()

        completed_btn = self.wait_for_element_link('Completed Tasks')
        completed_btn.click()

        task_list = self.wait_for_element_class('task-list').text
        self.assertNotIn('Buy bread', task_list)

        # they now go and check the box again for 'buy bread' and then delete the task
        # when they go back to completed tasks, buy bread is still listed as completed
        # even though it has been deleted from current task list
        current_btn = self.wait_for_element_link('Current Tasks')
        current_btn.click()

        checkbox = self.wait_for_element_class('checkbox-btn')
        checkbox.click()

        delete_input = self.wait_for_element_id('delete-task')
        delete_btn = self.wait_for_element_id('delete-btn')

        delete_input.send_keys(1)
        delete_btn.send_keys(Keys.ENTER)

        time.sleep(2)
        completed_btn = self.wait_for_element_link('Completed Tasks')
        completed_btn.click()

        task_list = self.wait_for_element_class('task-list').text
        self.assertIn('Buy bread', task_list)
