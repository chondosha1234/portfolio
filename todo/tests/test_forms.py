from django.test import TestCase
from django.contrib.auth import get_user_model

from todo.forms import (
    CheckBoxForm, TaskForm, NewListForm,
    ExistingListTaskForm, DeleteForm, EditForm
    )
from todo.models import Task, List

User = get_user_model()


class TaskFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = TaskForm()
        self.assertIn('placeholder="Enter a To Do Task"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = TaskForm(data={'text': ''})
        self.assertFalse(form.is_valid())


class NewListFormTest(TestCase):
    pass


class ExistingListTaskFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListTaskForm(for_list=list_)
        self.assertIn('placeholder="Enter a To Do Task"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListTaskForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Task.objects.create(list=list_, text='no twins')
        form = ExistingListTaskForm(for_list=list_, data={'text': 'no twins'})
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListTaskForm(for_list=list_, data={'text': 'something'})
        new_item = form.save()
        self.assertEqual(new_item, Task.objects.all()[0])


class DeleteFormTest(TestCase):

    def test_form_renders_delete_input(self):
        form = DeleteForm()
        self.assertIn('placeholder="Enter ID to delete..."', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = DeleteForm(data={'task_id': ''})
        self.assertFalse(form.is_valid())
        

class EditFormTest(TestCase):

    def test_form_renders_delete_input(self):
         form = DeleteForm()
         self.assertIn('placeholder="Enter ID to delete..."', form.as_p())

    def test_form_validation_for_blank_task_id(self):
        form = EditForm(data={'task_id': '', 'text': 'some change'})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_text_change(self):
        list_ = List.objects.create()
        Task.objects.create(list=list_, text='task')
        form = EditForm(data={'task_id': '1', 'text': ''})
        self.assertFalse(form.is_valid())
