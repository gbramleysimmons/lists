from django.urls import path
from .views import ViewList, AddItem, NewList, ValidateList, DeleteItem, ClearList, docs

urlpatterns = [
    path('newlist', NewList.as_view()),
    path('viewlist', ViewList.as_view()),
    path('additem', AddItem.as_view()),
    path('deleteitem', DeleteItem.as_view()),
    path('validatelist', ValidateList.as_view()),
    path('clearlist', ClearList.as_view()),
    path('', docs)

]
