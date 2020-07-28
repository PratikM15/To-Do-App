from django.contrib.auth.models import User
from django.db import models
import django.utils.timezone
import datetime
from datetime import date


# Create your models here.
class Task(models.Model):
    task_id = models.CharField(max_length=50)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    deadline = models.DateTimeField(default=None)

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.username.username
