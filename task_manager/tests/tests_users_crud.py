from .conftest import CustomTestCase
from django.urls import reverse
from task_manager.users.views import (
    UserCreateView, UserUpdateView, UserDeleteView)


class UsersTestCase(CustomTestCase):
    data_json = 'users-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]

    def test_users(self):
        self.url_contains_data_test(
            "users_index", self.data["users_expected"])

    def test_create(self):
        response = self.client.post(
            reverse("users_create"), self.data["create"], follow=True)
        self.redirect_with_message_test(
            response, "login", UserCreateView.message_success)
        self.url_contains_data_test(
            "users_index", self.data["create_expected"])

# users_update tests:

    def test_update_unlogin(self):
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", UserUpdateView.message_not_authenticated)

    def test_update_not_same_user(self):
        self.make_login_not_same_user()
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]), follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserUpdateView.message_not_same_user)

    def test_update_same_user(self):
        self.make_login_same_user()
        response = self.client.get(
            reverse("users_update", args=[self.update_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("users_update", args=[self.update_pk,]),
            self.data["update"],
            follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserUpdateView.message_success)
        self.url_contains_data_test(
            "users_index", self.data["update_expected"])

# users_delete tests:

    def test_delete_unlogin(self):
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", UserDeleteView.message_not_authenticated)

    def test_delete_not_same_user(self):
        self.make_login_not_same_user()
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]), follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserDeleteView.message_not_same_user)

    def test_delete_same_user(self):
        self.make_login_same_user()
        response = self.client.get(
            reverse("users_delete", args=[self.delete_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("users_delete", args=[self.delete_pk,]),
            self.data["delete"],
            follow=True)
        self.redirect_with_message_test(
            response, "users_index", UserDeleteView.message_success)
        self.url_contains_data_test(
            "users_index", self.data["delete_expected"])
