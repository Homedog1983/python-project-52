from django.test import tag
from task_manager.tests.conftests import CustomTestCase
from task_manager.users.views import (
    UserCreateView, UserUpdateView, UserDeleteView)


@tag("users")
class UsersTestCase(CustomTestCase):
    data_json = 'users-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.not_creator = self.auth["not_creator"]
        self.creator = self.auth["creator"]
        self.delete_pk_task_used = self.data["delete_task_used"]["pk"]
        self.task_used = self.auth["task_used"]

# users_index tests:

    def test_users(self):
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_create(self):
        self.url_post_data_redirect_test(
            "users_create", None, self.data["create"],
            "login", UserCreateView.success_message)
        self.url_get_data_test(
            "users_index", expected_data=self.data["create_expected"])

# users_update tests:

    def test_user_update_unlogined(self):
        self.url_get_redirect_test(
            "users_update", self.update_pk,
            "login", UserUpdateView.message_not_authenticated)

    def test_user_update_not_creator(self):
        self.make_login(self.not_creator)
        self.url_get_redirect_test(
            "users_update", self.update_pk,
            "users_index", UserUpdateView.message_not_creator)
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_update_creator(self):
        self.make_login(self.creator)
        self.url_get_test("users_update", self.update_pk)
        self.url_post_data_redirect_test(
            "users_update", self.update_pk, self.data["update"],
            "users_index", UserUpdateView.success_message)
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# users_delete tests:

    def test_user_delete_unlogined(self):
        self.url_get_redirect_test(
            "users_delete", self.delete_pk,
            "login", UserDeleteView.message_not_authenticated)

    def test_user_delete_not_creator(self):
        self.make_login(self.not_creator)
        self.url_get_redirect_test(
            "users_delete", self.delete_pk,
            "users_index", UserDeleteView.message_not_creator)
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_delete_creator_task_unused(self):
        self.make_login(self.creator)
        self.url_get_test("users_delete", self.delete_pk)
        self.url_post_data_redirect_test(
            "users_delete", self.delete_pk, self.data["delete"],
            "users_index", UserDeleteView.success_message)
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_user_delete_creator_task_used(self):
        self.make_login(self.task_used)
        self.url_get_test("users_delete", self.delete_pk_task_used)
        self.url_post_data_redirect_test(
            "users_delete", self.delete_pk_task_used, self.data["delete"],
            "users_index", UserDeleteView.message_used_object)
        self.url_get_data_test(
            "users_index",
            expected_data=self.data["users_expected"])
