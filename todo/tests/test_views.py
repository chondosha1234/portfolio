from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape
from unittest import skip

from todo.models import List, Task
from todo.forms import TaskForm, ExistingListTaskForm, DUPLICATE_TASK_ERROR


class ToDoHomeTest(TestCase):

    def test_page_renders_todo_home(self):
        response = self.client.get('/todo/')
        self.assertEquals(response.templates[0].name, 'todo_list.html')
        self.assertTemplateUsed(response, 'todo_list.html')


class ListViewTest(TestCase):

    def test_uses_todo_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/todo/{list_.id}')
        self.assertTemplateUsed(response, 'todo_list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/todo/{correct_list.id}')

        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_list(self):
        correct_list = List.objects.create()
        Task.objects.create(text='item 1', list=correct_list)
        Task.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Task.objects.create(text='other list 1', list=other_list)
        Task.objects.create(text='other list 2', list=other_list)

        response = self.client.get(f'/todo/{correct_list.id}')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other list 1')
        self.assertNotContains(response, 'other list 2')

    def test_can_save_post_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/todo/{correct_list.id}',
            data={'text': 'A new item for existing list'}
        )
        self.assertEqual(Task.objects.count(), 1)
        new_item = Task.objects.first()
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)


    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/todo/{list_.id}', data={'text': ''})

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Task.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['add_form'], ExistingListTaskForm)

    def test_duplicate_validation_error_ends_on_list_page(self):
        list1 = List.objects.create()
        item1 = Task.objects.create(list=list1, text='textey')
        response = self.client.post(f'/todo/{list1.id}', data={'text': 'textey'})

        expected_error = escape(DUPLICATE_TASK_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'todo_list.html')
        self.assertEqual(Task.objects.all().count(), 1)


class NewListIntegratedTest(TestCase):

    def test_save_post_request(self):
        self.client.post('/todo/new', data={'text': 'A new list item'})

        self.assertEqual(Task.objects.count(), 1)
        new_item = Task.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        response = self.client.post('/todo/new', data={'text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        new_list = Task.objects.first()
        self.assertEqual(response['location'], f'/todo/{new_list.id}')
        self.assertRedirects(response, f'/todo/{new_list.id}')

    def test_invalid_input_renders_home(self):
        response = self.client.post('/todo/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/todo/new', data={'text': ''})

        self.assertIsInstance(response.context['add_form'], TaskForm)

    def test_invalid_list_item_arent_saved(self):
        self.client.post('/todo/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)
