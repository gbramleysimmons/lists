from django.db import models
from django.contrib.auth.models import AbstractUser


# Records a list id
class List(models.Model):
    list_id = models.CharField(max_length=8, primary_key=True)


# Records a list item associated with a list id
class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)

