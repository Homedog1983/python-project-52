from task_manager.tests.conftests import CustomTestCase
from django.urls import reverse
from task_manager.tasks.views import (
    TaskIndexView, TaskCreateView, TaskUpdateView, TaskDeleteView)


class UsersTestCase(CustomTestCase):
    pass
    data_json = 'tasks-data.json'

    def setUp(self):
        super().setUp()

        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.task_logined = self.auth["task_logined"]
        self.logined_create = self.auth["logined_create"]
        self.logined_update = self.auth["logined_update"]
        self.not_creator_delete = self.auth["not_creator_delete"]
        self.creator_delete = self.auth["creator_delete"]

    # tasks_index tests:

    def test_tasks_unlogined(self):
        response = self.client.get(
            reverse("tasks_index"), follow=True)
        self.redirect_with_message_test(
            response, "login", TaskIndexView.message_not_authenticated)

    def test_tasks_logined(self):
        self.make_login(self.task_logined)
        self.url_data_test(
            "tasks_index", expected_data=self.data["tasks_expected"])

# tasks_create tests:

    def test_task_create_unlogined(self):
        response = self.client.get(
            reverse("tasks_create"), follow=True)
        self.redirect_with_message_test(
            response, "login", TaskCreateView.message_not_authenticated)

    def test_task_create_logined(self):
        self.make_login(self.logined_create)
        response = self.client.post(
            reverse("tasks_create"), self.data["create"], follow=True)
        self.redirect_with_message_test(
            response, "tasks_index", TaskCreateView.message_success)
        self.url_data_test(
            "tasks_index", expected_data=self.data["create_expected"])

# tasks_update tests:

    def test_task_update_unlogined(self):
        response = self.client.get(
            reverse("tasks_update", args=[self.update_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", TaskUpdateView.message_not_authenticated)

    def test_task_update_logined(self):
        self.make_login(self.logined_update)
        response = self.client.get(
            reverse("tasks_update", args=[self.update_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("tasks_update", args=[self.update_pk,]),
            self.data["update"],
            follow=True)
        self.redirect_with_message_test(
            response, "tasks_index", TaskUpdateView.message_success)
        self.url_data_test(
            "tasks_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# tasks_delete tests:
    def test_task_delete_unlogined(self):
        response = self.client.get(
            reverse("tasks_delete", args=[self.delete_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", TaskDeleteView.message_not_authenticated)

    def test_task_delete_logined_not_creator(self):
        self.make_login(self.not_creator_delete)
        response = self.client.get(
            reverse("tasks_delete", args=[self.delete_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "tasks_index", TaskDeleteView.message_not_creator)

    def test_task_delete_logined_creator(self):
        self.make_login(self.creator_delete)
        response = self.client.get(
            reverse("tasks_delete", args=[self.delete_pk,]),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("tasks_delete", args=[self.delete_pk,]),
            self.data["delete"],
            follow=True)
        self.redirect_with_message_test(
            response, "tasks_index", TaskDeleteView.message_success)
        self.url_data_test(
            "tasks_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])
