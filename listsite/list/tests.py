from django.test import TestCase
from . import models
from rest_framework.test import APIClient
import json


# Tests the models
class ListTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        my_list = models.List(list_id="000000")
        my_list.save()
        apples = models.ListItem(list=my_list, item="apples")
        oranges = models.ListItem(list=my_list, item="oranges")
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
        self.assertEqual(items[1].item, "oranges")


# Tests the API endpoints
class APITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        my_list = models.List(list_id="000000")
        my_list.save()
        apples = models.ListItem(list=my_list, item="apples")
        oranges = models.ListItem(list=my_list, item="oranges")
        apples.save()
        oranges.save()
        cls.client = APIClient()

    def testNewList(self):
        response = self.client.post("/newlist")
        self.assertEqual(response.status_code, 200)
        self.assertIn('list_id', response.data)
        self.assertEqual(len(response.data['list_id']), 6)

    def testValidateList(self):
        # Tests valid list
        body = {"list_id": "000000"}
        response = self.client.post("/validatelist", body, headers={'content-type': 'application/json'})
        self.assertTrue(response.status_code, 200)
        self.assertIn("exists", response.data)
        self.assertTrue(response.data["exists"])

        # Tests invalid list
        body = {"list_id": "000001"}
        response = self.client.post("/validatelist", body, headers={'content-type': 'application/json'})
        self.assertIn("exists", response.data)
        self.assertFalse(response.data["exists"])

        # Test malformed request
        response = self.client.post("/validatelist", {}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

    def testViewList(self):

        # Tests valid list
        body = {"list_id": "000000"}
        response = self.client.post("/viewlist", body, headers={'content-type': 'application/json'})
        self.assertTrue(response.status_code, 200)
        self.assertIn("list_items", response.data)
        list_items = response.data["list_items"]

        self.assertEqual(len(list_items), 2)
        self.assertEqual(list_items[0]['item'], "apples")
        self.assertEqual(list_items[1]['item'], "oranges")

        # Tests invalid list
        body = {"list_id": "000001"}
        response = self.client.post("/viewlist", body, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)


        # Test malformed request
        response = self.client.post("/viewlist", {}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

    def testAddItem(self):
        # Makes request
        body = {"list_id": "000000", 'item': "bananas"}
        response = self.client.post("/additem", body, headers={'content-type': 'application/json'})
        self.assertTrue(response.status_code, 200)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["id"], 3)
        self.assertIn("list", response.data)
        self.assertEqual(response.data["list"], "000000")
        self.assertIn("item", response.data)
        self.assertEqual(response.data["item"], "bananas")

        # Checks to make sure request processed
        body = {"list_id": "000000"}
        view_response = self.client.post("/viewlist", body, headers={'content-type': 'application/json'})
        list_items = view_response.data["list_items"]
        self.assertEqual(list_items[2], response.data)

        # Tests invalid list id
        body = {"list_id": "000001"}
        response = self.client.post("/additem", body, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

        # Test malformed request
        response = self.client.post("/additem", {}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

    def testDeleteItem(self):
        # Makes request
        body = {"list_id": "000000", 'item': "apples"}
        response = self.client.post("/deleteitem", body, headers={'content-type': 'application/json'})
        self.assertTrue(response.status_code, 200)
        self.assertIsNone(response.data)

        # Checks to make sure request processed
        body = {"list_id": "000000"}
        view_response = self.client.post("/viewlist", body, headers={'content-type': 'application/json'})
        list_items = view_response.data["list_items"]
        self.assertEqual(len(list_items), 1)
        # self.assertEqual(list_items[0]["item"], "oranges")

        # Tests invalid list id
        body = {"list_id": "000001", "item": "apples"}
        response = self.client.post("/deleteitem", body, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

        # Test malformed request
        response = self.client.post("/deleteitem", {}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

        # Test item that doesn't exist
        response = self.client.post("/deleteitem", {"list_id": "000000", "item": "grapes"}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

    def testClearList(self):
        body = {"list_id": "000000"}
        response = self.client.post("/clearlist", body, headers={'content-type': 'application/json'})
        self.assertTrue(response.status_code, 200)
        self.assertIsNone(response.data)

        body = {"list_id": "000000"}
        view_response = self.client.post("/viewlist", body, headers={'content-type': 'application/json'})
        list_items = view_response.data["list_items"]
        self.assertEqual(len(list_items), 0)

        body = {"list_id": "000001"}
        response = self.client.post("/clearlist", body, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

        # Test malformed request
        response = self.client.post("/clearlist", {}, headers={'content-type': 'application/json'})
        self.assertIn("error", response.data)

