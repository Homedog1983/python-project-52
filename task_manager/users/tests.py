from django.test import tag
from task_manager.tests.conftests import BaseTestCase
from task_manager.users.views import (
    UserCreateView, UserUpdateView, UserDeleteView)


@tag("users")
class UsersTestCase(BaseTestCase):
    data_json = 'users-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.not_creator = self.auth["not_creator"]
        self.creator = self.auth["creator"]
        self.delete_pk_used_in_task = self.data["delete_used_in_task"]["pk"]
        self.used_in_task = self.auth["used_in_task"]

# users_index tests:

    def test_get_users(self):
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["users_expected"])

# users_create tests:

    def test_post_users_create(self):
        self.check_for_redirect_with_message_after_post_request(
            "users_create", None, self.data["create"],
            "login", UserCreateView.success_message)
        self.check_for_response_data_after_get_request(
            "users_index", expected_data=self.data["create_expected"])

# users_update tests:

    def test_get_users_update_by_unlogged(self):
        self.check_for_redirect_with_message_after_get_request(
            "users_update", self.update_pk,
            "login", UserUpdateView.message_not_authenticated)

    def test_get_users_update_by_logged_not_creator(self):
        self.make_logged_as(self.not_creator)
        self.check_for_redirect_with_message_after_get_request(
            "users_update", self.update_pk,
            "users_index", UserUpdateView.message_not_creator)
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_dispatch_users_update_by_logged_creator(self):
        self.make_logged_as(self.creator)
        self.check_for_status_code_after_get_request(
            "users_update", self.update_pk)
        self.check_for_redirect_with_message_after_post_request(
            "users_update", self.update_pk, self.data["update"],
            "users_index", UserUpdateView.success_message)
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# users_delete tests:

    def test_get_users_delete_by_unlogged(self):
        self.check_for_redirect_with_message_after_get_request(
            "users_delete", self.delete_pk,
            "login", UserDeleteView.message_not_authenticated)

    def test_dispatch_users_delete_by_logged_not_creator(self):
        self.make_logged_as(self.not_creator)
        self.check_for_redirect_with_message_after_get_request(
            "users_delete", self.delete_pk,
            "users_index", UserDeleteView.message_not_creator)
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_dispatch_users_delete_by_logged_creator_with_user_unused_in_task(
            self):
        self.make_logged_as(self.creator)
        self.check_for_status_code_after_get_request(
            "users_delete", self.delete_pk)
        self.check_for_redirect_with_message_after_post_request(
            "users_delete", self.delete_pk, self.data["delete"],
            "users_index", UserDeleteView.success_message)
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_dispatch_users_delete_by_logged_creator_with_user_used_in_task(
            self):
        self.make_logged_as(self.used_in_task)
        self.check_for_status_code_after_get_request(
            "users_delete", self.delete_pk_used_in_task)
        self.check_for_redirect_with_message_after_post_request(
            "users_delete",
            self.delete_pk_used_in_task, self.data["delete"],
            "users_index", UserDeleteView.message_used_object)
        self.check_for_response_data_after_get_request(
            "users_index",
            expected_data=self.data["users_expected"])
