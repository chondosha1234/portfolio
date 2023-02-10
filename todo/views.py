from django.shortcuts import render, redirect
from django.views.generic import ListView
#from django.contrib.auth import get_user_model

from todo.models import Task, List, Completed
from todo.forms import CheckBoxForm, TaskForm, ExistingListTaskForm

#User = get_user_model()

# Create your views here.
def todo_list(request):
    return render(request, 'todo_list.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListTaskForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListTaskForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()

    tasks = Task.objects.filter(list=list_)
    tasks_forms = []
    for t in tasks:
        task_form = CheckBoxForm(complete=t.complete, text=t.text, id=t.id)
        tasks_forms.append(task_form)
    context = {
        'list': list_,
        'tasks_forms': tasks_forms
    }
    return render(request, 'todo_list.html', context)

def new_list(request):
    return render(request, 'todo_list.html')

def delete_task(request):
    pass

def edit_task(request):
    pass

def completed_tasks(request):
    pass

"""
class ToDoListView(ListView):
    model = Task
    template_name = 'todo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(request)
        list_ = List.objects.get(id=list_id)
        tasks = Task.objects.filter(list=list_)
        tasks_forms = []
        for t in tasks:
            task_form = CheckBoxForm(complete=t.complete, text=t.text, id=t.id)
            tasks_forms.append(task_forms)
        context['list'] = list_
        context['tasks_forms'] = tasks_forms
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)
"""
