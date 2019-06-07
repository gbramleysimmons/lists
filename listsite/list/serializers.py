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
