# Generated by Django 3.2.13 on 2023-02-11 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_list_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed',
            name='list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='todo.list'),
        ),
    ]