from django.db import models

# Create your models here.
class List(models.Model):
    pass

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
    description = models.CharField(max_length=64)
    task_id = models.IntegerField()
