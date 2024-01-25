from json import load as json_load
from os.path import splitext
from task_manager.settings import BASE_DIR
from django.urls import reverse
from task_manager.users.models import CustomUser
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


class BaseTestCase(TestCase):
    fixtures = [
        "users-db.json",
        "statuses-db.json",
        "tasks-db.json",
        "labels-db.json"
    ]
    data_json = ''
    auth = get_content_from("users_auth.json")
    data = {}
    client = Client()

    def setUp(self):
        self.data = get_content_from(self.data_json)

    def make_logged_as(self, username):
        user = CustomUser.objects.get(username=username)
        self.client.force_login(user)

    def get_message(self, response):
        return list(response.context.get("messages"))[0].message

    def check_for_status_code_after_get_request(
            self, request_url_name, pk, status_code=200):
        args = [pk, ] if pk else []
        response = self.client.get(reverse(request_url_name, args=args))
        self.assertEqual(response.status_code, status_code)

    def check_for_redirect_with_message_in_response(
            self, response, expected_url_name, expected_message):
        self.assertEqual(expected_message, self.get_message(response))
        self.assertRedirects(
            response, reverse(expected_url_name), status_code=302,
            target_status_code=200, fetch_redirect_response=True)

    def check_for_redirect_with_message_after_get_request(
            self, request_url_name, pk, redirect_url_name, expected_message):
        args = [pk, ] if pk else []
        response = self.client.get(
            reverse(request_url_name, args=args), follow=True)
        self.check_for_redirect_with_message_in_response(
            response, redirect_url_name, expected_message)

    def check_for_redirect_with_message_after_post_request(
            self, request_url_name, pk, post_data,
            redirect_url_name, message_expected):
        args = [pk, ] if pk else []
        response = self.client.post(
            reverse(request_url_name, args=args), post_data, follow=True)
        self.check_for_redirect_with_message_in_response(
            response, redirect_url_name, message_expected)

    def check_for_response_data_after_get_request(
            self, request_url_name, get_data={}, expected_data=[],
            not_expected_data=[]):
        response = self.client.get(reverse(request_url_name), get_data)
        for elem in expected_data:
            self.assertContains(response, elem, status_code=200)
        for elem in not_expected_data:
            self.assertNotContains(response, elem, status_code=200)
