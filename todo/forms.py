from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from todo.models import Task, List

DUPLICATE_TASK_ERROR = "You've already got this in your list"

class TaskForm(forms.models.ModelForm):

    class Meta:
        model = Task
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a To Do Task',
                'class': 'form-control',
                'id': 'add-item'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Add Task'


class NewListForm(TaskForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])


class ExistingListTaskForm(TaskForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_TASK_ERROR]}
            self._update_errors(e)


class DeleteForm(forms.Form):

    task_id = forms.IntegerField(
        label="Delete Task",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter ID to delete...',
                'id': 'delete-task'
            }
        )
    )


class EditForm(forms.Form):

    task_id = forms.IntegerField(
        label="Edit Task",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter ID to edit...',
                'id': 'edit-task-id'
            }
        )
    )

    text = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter new text...',
                'id': 'edit-task-text'
            }
        )
    )


class CheckBoxForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['complete']

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text')
        self.id = kwargs.pop('id')
        self.complete = kwargs.pop('complete')
        super(CheckBoxForm, self).__init__(*args, **kwargs)
        self.fields['complete'] = forms.BooleanField(label="", widget=forms.CheckboxInput(attrs={'class': 'checkbox-btn', 'onclick':'this.form.submit();'}), required=False)
        if (self.complete):
            self.fields['complete'].initial = True
        else:
            self.fields['complete'].initial = False
