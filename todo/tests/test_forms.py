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
        self.assertIn('placeholder="Enter a Task"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = TaskForm(data={'text': ''})
        self.assertFalse(form.is_valid())


class NewListFormTest(TestCase):
    pass


class ExistingListTaskFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListTaskForm(for_list=list_)
        self.assertIn('placeholder="Enter a Task"', form.as_p())

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
        list_ = List.objects.create()
        form = DeleteForm(for_list=list_)
        self.assertIn('placeholder="Enter ID to delete..."', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = DeleteForm(data={'task_id': ''}, for_list=list_)
        self.assertFalse(form.is_valid())

    def test_form_returns_error_if_id_does_not_exist(self):
        list_ = List.objects.create()
        task = Task.objects.create(list=list_, text='test task')
        form = DeleteForm(data={'task_id': '2'}, for_list=list_)
        self.assertEqual(task.id, 1)
        self.assertFalse(form.is_valid())

    def test_form_validation_error_if_id_on_different_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        task = Task.objects.create(list=list1, text='task')
        form = DeleteForm(data={'task_id': '1'}, for_list=list2)
        self.assertEqual(task.id, 1)
        self.assertFalse(form.is_valid())

    def test_delete_on_other_list_does_not_remove_task(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        task = Task.objects.create(list=list1, text='task')
        self.assertEqual(Task.objects.count(), 1)
        form = DeleteForm(data={'task_id': '1'}, for_list=list2)
        self.assertEqual(Task.objects.count(), 1)


class EditFormTest(TestCase):

    def test_form_renders_edit_input(self):
        list_ = List.objects.create()
        form = EditForm(for_list=list_)
        self.assertIn('placeholder="Enter ID to edit..."', form.as_p())

    def test_form_validation_for_blank_task_id(self):
        list_ = List.objects.create()
        form = EditForm(data={'task_id': '', 'text': 'some change'}, for_list=list_)
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_text_change(self):
        list_ = List.objects.create()
        Task.objects.create(list=list_, text='task')
        form = EditForm(data={'task_id': '1', 'text': ''}, for_list=list_)
        self.assertFalse(form.is_valid())

    def test_form_returns_error_if_id_does_not_exist(self):
        list_ = List.objects.create()
        task = Task.objects.create(list=list_, text='test task')
        form = EditForm(data={'task_id': '', 'text': 'some change'}, for_list=list_)
        self.assertEqual(task.id, 1)
        self.assertFalse(form.is_valid())

    def test_form_validation_error_if_id_on_different_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        task = Task.objects.create(list=list1, text='task')
        form = EditForm(data={'task_id': '1', 'text': 'some change'}, for_list=list2)
        self.assertEqual(task.id, 1)
        self.assertFalse(form.is_valid())

    def test_edit_on_other_list_does_not_change_task(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        task = Task.objects.create(list=list1, text='task')
        self.assertEqual(task.text, 'task')
        form = EditForm(data={'task_id': '1', 'text': 'some change'}, for_list=list2)
        self.assertEqual(task.text, 'task')
