from django.test import tag
from task_manager.tests.conftests import CustomTestCase
from task_manager.tasks.views import (
    TaskIndexView, TaskCreateView, TaskUpdateView, TaskDeleteView)


@tag("tasks")
class TasksTestCase(CustomTestCase):
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
        self.url_get_redirect_test(
            "tasks_index", None,
            "login", TaskIndexView.message_not_authenticated)

    def test_tasks_logined(self):
        self.make_login(self.task_logined)
        self.url_get_data_test(
            "tasks_index", expected_data=self.data["tasks_expected"])

# tasks_create tests:

    def test_task_create_unlogined(self):
        self.url_get_redirect_test(
            "tasks_create", None,
            "login", TaskCreateView.message_not_authenticated)

    def test_task_create_logined(self):
        self.make_login(self.logined_create)
        self.url_post_data_redirect_test(
            "tasks_create", None, self.data["create"],
            "tasks_index", TaskCreateView.message_success)
        self.url_get_data_test(
            "tasks_index",
            expected_data=self.data["create_expected"])

# tasks_update tests:

    def test_task_update_unlogined(self):
        self.url_get_redirect_test(
            "tasks_update", self.update_pk,
            "login", TaskUpdateView.message_not_authenticated)

    def test_task_update_logined(self):
        self.make_login(self.logined_update)
        self.url_get_test("tasks_update", self.update_pk)
        self.url_post_data_redirect_test(
            "tasks_update", self.update_pk, self.data["update"],
            "tasks_index", TaskUpdateView.message_success)
        self.url_get_data_test(
            "tasks_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# tasks_delete tests:
    def test_task_delete_unlogined(self):
        self.url_get_redirect_test(
            "tasks_delete", self.delete_pk,
            "login", TaskDeleteView.message_not_authenticated)

    def test_task_delete_logined_not_creator(self):
        self.make_login(self.not_creator_delete)
        self.url_get_redirect_test(
            "tasks_delete", self.delete_pk,
            "tasks_index", TaskDeleteView.message_not_creator)

    def test_task_delete_logined_creator(self):
        self.make_login(self.creator_delete)
        self.url_get_test("tasks_delete", self.update_pk)
        self.url_post_data_redirect_test(
            "tasks_delete", self.delete_pk, self.data["delete"],
            "tasks_index", TaskDeleteView.message_success)
        self.url_get_data_test(
            "tasks_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])
