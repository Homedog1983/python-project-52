from json import load as json_load
from os.path import splitext
from task_manager.settings import BASE_DIR
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


FIXTURES = f'{BASE_DIR}/task_manager/tests/fixtures'


def get_full_path(file_name):
    return f"{FIXTURES}/{file_name}"


def get_content_from(path):
    full_path = get_full_path(path)
    _, extension = splitext(full_path)
    with open(full_path) as content_file:
        if extension == '.json':
            result = json_load(content_file)
        else:
            raise ValueError('Unsupported file format')
    return result


class CustomTestCase(TestCase):
    fixtures = [
        "users-db.json",
        "statuses-db.json"]
    data_json = ''
    auth = get_content_from("users_auth.json")
    data = {}
    client = Client()

    def setUp(self):
        self.data = get_content_from(self.data_json)

    def url_contains_data_test(self, url_name, expected_data: list):
        response = self.client.get(reverse(url_name))
        for elem in expected_data:
            self.assertContains(response, elem, count=1, status_code=200)

    def get_message(self, response):
        return list(response.context.get("messages"))[0].message

    def redirect_with_message_test(
            self, response, expected_url_name, expected_message):
        self.assertEqual(expected_message, self.get_message(response))
        self.assertRedirects(
            response, reverse(expected_url_name), status_code=302,
            target_status_code=200, fetch_redirect_response=True)

    def make_login_not_same_user(self):
        user = User.objects.get(username=self.auth["not_same_user"])
        self.client.force_login(user)

    def make_login_same_user(self):
        user = User.objects.get(username=self.auth["same_user"])
        self.client.force_login(user)
