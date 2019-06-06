from django.shortcuts import render
from rest_framework import viewsets, views, response, generics
from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
import random, string
from django.db.models import Q
from . import models, serializers

# Generates a random 6 character id for the lists
def gen_random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))


# Endpoint to create a new list
class NewList(views.APIView):

    def post(self, request, format=None):
        new_list = models.List(list_id=gen_random_id())
        new_list.save()
        return response.Response({"list_id": new_list.list_id})


# Endpoint to add a new item to a list
class NewItem(views.APIView):

    def post(self, request, format=None):
        list_id = request.data['list_id']
        my_list = models.List.objects.filter(pk=list_id)[0]
        new_item = models.ListItem()
        new_item.list = my_list
        new_item.item = request.data['item']
        new_item.save()
        return response.Response(serializers.ListItemSerializer(new_item).data)


class DeleteItem(views.APIView):
    def post(self, request, format=None):
        list_id = request.data['list_id']
        item = request.data['item']
        try:
            models.ListItem.objects.filter(Q(list_id=list_id) & Q(item=item)).delete()
            return response.Response()

        except models.ListItem.DoesNotExist:
            return response.Response({"error": "Item doesn't exist"})


class ClearList(views.APIView):
    def post(self, request, format=None):
        list_id = request.data['list_id']
        curr_list = get_object_or_404(models.List, pk=list_id)
        curr_list.listitem_set.all().delete()
        return response.Response()


class ViewList(views.APIView):

    def post(self, request, format=None):
        list_id = request.data['list_id']
        list_items = map(lambda item: models.ListItemSerializer(item).data, models.ListItem.objects.filter(list_id=list_id))
        return response.Response({"list_items": list_items})


class ValidateList(views.APIView):
    def post(self, request, format=None):
        list_id = request.data['list_id']
        try:
            List.objects.get(pk=list_id)
            return response.Response({"exists": True})
        except List.DoesNotExist:
            return response.Response({"exists": False})

class Signup(views.APIView):
    def post(self, request, format=None):
        if len(models.CustomUser.objects.filter(pk=request.data["username"])) != 0:
            return response.Response({"error": "Bad username"})
        else:
            user = models.CustomUser(username=request.data['phone_number'])
            user.phone_number = request.data['phone_number']
            user.email = request.data['email']
            user.password = request.data['password']
            user.save()
            return response.Response({"success": True})


class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer