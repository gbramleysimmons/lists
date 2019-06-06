from rest_framework import serializers
from . import models

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        fields = "__all__"


class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ListItem
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserList
        fields = ('list_id', 'username')

