from django.db import models
from django.contrib.auth.models import AbstractUser



# Records a list id

class List(models.Model):
    list_id = models.CharField(max_length=8, primary_key=True)


# Records a list item associated with a list id
class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)


# Models a user, with associated username, password, phone number, and
# email. All fields except username are encrypted
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12, default="0000000000")
    def __str__(self):
        return self.username

# A junction table for lists and users
class UserList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)


