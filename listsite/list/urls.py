from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import ViewList, NewItem, NewList, ValidateList, DeleteItem, ClearList
from . import views

urlpatterns = [
    path('newlist', NewList.as_view()),
    path('viewlist', ViewList.as_view()),
    path('additem', NewItem.as_view()),
    path('deleteitem', DeleteItem.as_view()),
    path('validatelist', ValidateList.as_view()),
    path('clearlist', ClearList.as_view()),
    path('users', views.UserListView.as_view()),

]
