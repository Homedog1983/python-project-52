from django.test import tag
from task_manager.tests.conftests import BaseTestCase
from task_manager.tasks.views import (
    FilterIndexView, TaskCreateView, TaskUpdateView, TaskDeleteView)


@tag("tasks_crud")
class TasksTestCase(BaseTestCase):
    data_json = 'tasks-data.json'

    def setUp(self):
        super().setUp()

        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.logged = self.auth["tasks_logged"]
        self.logged_create = self.auth["logged_create"]
        self.logged_update = self.auth["logged_update"]
        self.not_creator_delete = self.auth["not_creator_delete"]
        self.creator_delete = self.auth["creator_delete"]

# tasks_index tests:

    def test_get_tasks_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "tasks_index", None,
            "login", FilterIndexView.message_not_authenticated)

    def test_get_tasks_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_response_data_after_get_request(
            "tasks_index", expected_data=self.data["tasks_expected"])

# tasks_create tests:

    def test_get_tasks_create_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "tasks_create", None,
            "login", TaskCreateView.message_not_authenticated)

    def test_post_tasks_create_by_logged(self):
        self.make_logged_as(self.logged_create)
        self.assert_redirect_with_message_after_post_request(
            "tasks_create", None, self.data["create"],
            "tasks_index", TaskCreateView.success_message)
        self.assert_response_data_after_get_request(
            "tasks_index",
            expected_data=self.data["create_expected"])

# tasks_update tests:

    def test_get_tasks_update_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "tasks_update", self.update_pk,
            "login", TaskUpdateView.message_not_authenticated)

    def test_dispatch_tasks_update_by_logged(self):
        self.make_logged_as(self.logged_update)
        self.assert_status_code_after_get_request(
            "tasks_update", self.update_pk)
        self.assert_redirect_with_message_after_post_request(
            "tasks_update", self.update_pk, self.data["update"],
            "tasks_index", TaskUpdateView.success_message)
        self.assert_response_data_after_get_request(
            "tasks_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# tasks_delete tests:

    def test_get_task_delete_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "tasks_delete", self.delete_pk,
            "login", TaskDeleteView.message_not_authenticated)

    def test_get_task_delete_by_logged_not_creator(self):
        self.make_logged_as(self.not_creator_delete)
        self.assert_redirect_with_message_after_get_request(
            "tasks_delete", self.delete_pk,
            "tasks_index", TaskDeleteView.message_not_creator)

    def test_dispatch_task_delete_by_logged_creator(self):
        self.make_logged_as(self.creator_delete)
        self.assert_status_code_after_get_request(
            "tasks_delete", self.update_pk)
        self.assert_redirect_with_message_after_post_request(
            "tasks_delete", self.delete_pk, self.data["delete"],
            "tasks_index", TaskDeleteView.success_message)
        self.assert_response_data_after_get_request(
            "tasks_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])


@tag("tasks_filter")
class TasksFilterTestCase(BaseTestCase):
    fixtures = [
        "users-db.json",
        "statuses-db.json",
        "tasks_filter-db.json",
        "labels-db.json"
    ]
    data_json = 'tasks_filter-data.json'

    def setUp(self):
        super().setUp()

        self.filter_url = "tasks_index"
        self.logged_1 = self.auth["tasks_logged_1"]
        self.logged_2 = self.auth["tasks_logged_2"]
        self.logged_3 = self.auth["tasks_logged_3"]

# all below by logged user

    def test_tasks_filter_without_filter(self):
        self.make_logged_as(self.logged_1)
        self.assert_response_data_after_get_request(
            "tasks_index", expected_data=self.data["initial_expected"])

    def test_tasks_filter_by_status_only(self):
        self.make_logged_as(self.logged_1)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["only_status"],
            expected_data=self.data["only_status_expected"],
            not_expected_data=self.data["only_status_not_expected"])

    def test_tasks_filter_by_executor_only(self):
        self.make_logged_as(self.logged_1)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["only_executor"],
            expected_data=self.data["only_executor_expected"],
            not_expected_data=self.data["only_executor_not_expected"])

    def test_tasks_filter_by_labels_only(self):
        self.make_logged_as(self.logged_1)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["only_labels"],
            expected_data=self.data["only_labels_expected"],
            not_expected_data=self.data["only_labels_not_expected"])

    def test_tasks_filter_by_creator_1_only(self):
        self.make_logged_as(self.logged_1)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_1_expected"],
            not_expected_data=self.data["self_tasks_1_not_expected"])

    def test_tasks_filter_by_creator_2_only(self):
        self.make_logged_as(self.logged_2)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_2_expected"],
            not_expected_data=self.data["self_tasks_2_not_expected"])

    def test_tasks_filter_by_creator_3_only(self):
        self.make_logged_as(self.logged_3)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_3_expected"],
            not_expected_data=self.data["self_tasks_3_not_expected"])

    def test_tasks_filter_by_creator_3_complex_1(self):
        self.make_logged_as(self.logged_3)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["complex_user_3_1"],
            expected_data=self.data["complex_user_3_1_expected"],
            not_expected_data=self.data["complex_user_3_1_not_expected"])

    def test_tasks_filter_by_creator_3_complex_2(self):
        self.make_logged_as(self.logged_3)
        self.assert_response_data_after_get_request(
            self.filter_url, get_data=self.data["complex_user_3_2"],
            expected_data=self.data["complex_user_3_2_expected"],
            not_expected_data=self.data["complex_user_3_2_not_expected"])
