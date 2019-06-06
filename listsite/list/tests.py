from django.test import TestCase
from . import models


class ListTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        my_list = models.List(list_id="000000")
        my_list.save()
        apples = models.ListItem(list=my_list, item="apples")
        oranges = models.ListItem(list=my_list, item="apples")
        apples.save()
        oranges.save()

    def testListInDatabase(self):
        lists = models.List.objects.all()
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0].list_id, "000000")

    def testListHasItems(self):
        my_list = models.List.objects.get(pk="000000")
        items = my_list.listitem_set.all()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].item, "apples")