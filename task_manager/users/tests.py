from task_manager.tests.conftests import CustomTestCase
from django.urls import reverse
from task_manager.users.views import (
    UserCreateView, UserUpdateView, UserDeleteView)


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

    def test_users(self):
        self.url_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_create(self):
        response = self.client.post(
            reverse("users_create"), self.data["create"], follow=True)
        self.redirect_with_message_test(
            response, "login", UserCreateView.message_success)
        self.url_data_test(
            "users_index", expected_data=self.data["create_expected"])

# users_update tests:

    def test_user_update_unlogined(self):
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", UserUpdateView.message_not_authenticated)

    def test_user_update_not_creator(self):
        self.make_login(self.not_creator)
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]), follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserUpdateView.message_not_creator)
        self.url_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_update_creator(self):
        self.make_login(self.creator)
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("users_update", args=[self.update_pk,]),
            self.data["update"],
            follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserUpdateView.message_success)
        self.url_data_test(
            "users_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# users_delete tests:

    def test_user_delete_unlogined(self):
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", UserDeleteView.message_not_authenticated)

    def test_user_delete_not_creator(self):
        self.make_login(self.not_creator)
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]), follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserDeleteView.message_not_creator)
        self.url_data_test(
            "users_index",
            expected_data=self.data["users_expected"])

    def test_user_delete_creator_task_unused(self):
        self.make_login(self.creator)
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("users_delete", args=[self.delete_pk,]),
            self.data["delete"],
            follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserDeleteView.message_success)
        self.url_data_test(
            "users_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_user_delete_creator_task_used(self):
        self.make_login(self.task_used)
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk_task_used,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("users_delete", args=[self.delete_pk_task_used,]),
            self.data["delete"],
            follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserDeleteView.message_used_object)
        self.url_data_test(
            "users_index",
            expected_data=self.data["users_expected"])