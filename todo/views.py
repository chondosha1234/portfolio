from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.models import Task, List, Completed
from todo.forms import (
    CheckBoxForm, TaskForm, NewListForm,
    ExistingListTaskForm, DeleteForm, EditForm
    )

User = get_user_model()


def todo_list(request):
    add_form = TaskForm()
    context = {
        'add_form': add_form
    }
    return render(request, 'todo_list.html', context)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    add_form = ExistingListTaskForm(for_list=list_)
    edit_form = EditForm()
    delete_form = DeleteForm()

    if request.method == 'POST':
        add_form = ExistingListTaskForm(for_list=list_, data=request.POST)
        if add_form.is_valid():
            add_form.save()

    tasks = Task.objects.filter(list=list_)
    tasks_forms = []
    for t in tasks:
        task_form = CheckBoxForm(complete=t.complete, text=t.text, id=t.id)
        tasks_forms.append(task_form)
    context = {
        'list': list_,
        'tasks_forms': tasks_forms,
        'add_form': add_form,
        'edit_form': edit_form,
        'delete_form': delete_form
    }
    return render(request, 'todo_list.html', context)


def new_list(request):
    add_form = NewListForm(data=request.POST)
    if add_form.is_valid():
        list_ = add_form.save(owner=request.user)
        return redirect(str(list_.get_absolute_url()))

    context = {
        'add_form': add_form
    }
    return render(request, 'todo_list.html', context)


def user_list(request, email):
    owner = User.objects.get(email=email)
    context = {
        'owner': owner
    }
    return render(request, 'user_lists.html', context)


def delete_task(request, list_id):
    list_ = List.objects.get(id=list_id)
    delete_form = DeleteForm(data=request.POST)
    if delete_form.is_valid():
        task = Task.objects.get(id=request.POST['task_id'])
        if task and task.list == list_:
            task.delete()

    return redirect('todo:view_list', list_id=list_id)


def edit_task(request, list_id):
    list_ = List.objects.get(id=list_id)
    edit_form = EditForm(data=request.POST)
    if edit_form.is_valid():
        task = Task.objects.get(id=request.POST['task_id'])
        if task and task.list == list_:
            task.text = request.POST['text']
            task.save()

    return redirect('todo:view_list', list_id=list_id)


def completed_tasks(request, list_id=None):
    tasks = Completed.objects.filter(list=list_id)
    context = {
        'tasks': tasks,
    }
    return render(request, 'completed.html', context)


def complete(request, id):
    task = Task.objects.get(pk=id)

    if 'complete' in request.POST:
        task.complete = True
        completed_task = Completed(description=task.description, task_id=id, list=task.list)
        completed_task.save()
    else:
        task.complete = False
        completed_task = Completed.objects.get(task_id=id)
        completed_task.delete()

    task.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
