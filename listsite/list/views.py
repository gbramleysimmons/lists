from rest_framework import views, response
from django.shortcuts import render
import random
import string
from django.db.models import Q
from . import models, serializers
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse


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
class AddItem(views.APIView):
    def post(self, request, format=None):
        try:
            list_id = request.data['list_id']
        except MultiValueDictKeyError:
            return response.Response({"error": "Invalid request format"})

        try:
            my_list = models.List.objects.get(pk=list_id)
        except models.List.DoesNotExist:
            return response.Response({"error": "List does not exist"})

        new_item = models.ListItem()
        new_item.list = my_list

        new_item.item = request.data['item']
        new_item.save()
        return response.Response(serializers.ListItemSerializer(new_item).data)


# Deletes an item from a list
class DeleteItem(views.APIView):
    def post(self, request, format=None):
        try:
            list_id = request.data['list_id']
            item = request.data['item']
        except MultiValueDictKeyError:
            return response.Response({"error": "Invalid request format"})
        try:
            my_list = models.List.objects.get(pk=list_id)
        except models.List.DoesNotExist:
            return response.Response({"error": "List does not exist"})
        try:
            models.ListItem.objects.get(Q(list=my_list) & Q(item=item)).delete()
            return response.Response()

        except models.ListItem.DoesNotExist:
            return response.Response({"error": "Item doesn't exist"})


# Clears a list
class ClearList(views.APIView):
    def post(self, request, format=None):
        try:
            list_id = request.data['list_id']
        except MultiValueDictKeyError:
            return response.Response({"error": "Invalid request format"})
        try:
            curr_list = models.List.objects.get(pk=list_id)
        except models.List.DoesNotExist:
            return response.Response({"error": "List does not exist"})
        curr_list.listitem_set.all().delete()
        return response.Response()


# Returns all items in a list
class ViewList(views.APIView):

    def post(self, request, format=None):
        try:
            list_id = request.data['list_id']
        except MultiValueDictKeyError:
            return response.Response({"error": "Invalid request format"})

        try:
            my_list = models.List.objects.get(pk=list_id)
        except models.List.DoesNotExist:
            return response.Response({"error": "List does not exist"})

        list_items = list(map(lambda item: serializers.ListItemSerializer(item).data,
                              models.ListItem.objects.filter(list=my_list)))
        return response.Response({"list_items": list_items})


# Checks if the database contains a list with the specified ID
class ValidateList(views.APIView):
    def post(self, request, format=None):
        try:
            list_id = request.data['list_id']
        except MultiValueDictKeyError:
            return response.Response({"error": "Invalid request format"})

        try:
            models.List.objects.get(pk=list_id)
            return response.Response({"exists": True})
        except models.List.DoesNotExist:
            return response.Response({"exists": False})


def docs(request):
    template = loader.get_template('list/docs.html')
    return HttpResponse(template.render({}, request))
