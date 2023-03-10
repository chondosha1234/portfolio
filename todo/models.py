from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        blank=True,
        null=True
    )

    @property
    def name(self):
        return self.task_set.first().text

    def get_absolute_url(self):
        return reverse('todo:view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Task.objects.create(text=first_item_text, list=list_)
        return list_


class Task(models.Model):
    text = models.CharField(max_length=64)
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text

class Completed(models.Model):
    text = models.CharField(max_length=64)
    task_id = models.IntegerField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
