from django.test import TestCase
from django.test import Client


class CustomTestCase(TestCase):
    # databases = {"TEST"}
    # fixtures = ["user-data.json"]
    fixtures = ["statuses-data.json", "users-data.json",]

    def setUp(self):
        self.client = Client()


class SomeTestCase(CustomTestCase):

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)



# from django.test import Client
# >>> c = Client()
# >>> response = c.post("/login/", {"username": "john", "password": "smith"})
# >>> response.status_code
# 200
# >>> response = c.get("/customer/details/")
# >>> response.content
