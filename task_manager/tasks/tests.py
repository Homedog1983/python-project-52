from django.test import tag
from task_manager.tests.conftests import CustomTestCase
from task_manager.tasks.views import (
    FilterIndexView, TaskCreateView, TaskUpdateView, TaskDeleteView)
# from django.urls import reverse


@tag("tasks_crud")
class TasksTestCase(CustomTestCase):
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
            "login", FilterIndexView.message_not_authenticated)

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


@tag("tasks_filter")
class TasksFilterTestCase(CustomTestCase):
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
        self.logined_1 = self.auth["task_logined_1"]
        self.logined_2 = self.auth["task_logined_2"]
        self.logined_3 = self.auth["task_logined_3"]

    def test_tf_logined(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            "tasks_index", expected_data=self.data["initial_expected"])

    def test_tf_only_status(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["only_status"],
            expected_data=self.data["only_status_expected"],
            not_expected_data=self.data["only_status_not_expected"])

    def test_tf_only_executor(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["only_executor"],
            expected_data=self.data["only_executor_expected"],
            not_expected_data=self.data["only_executor_not_expected"])

    def test_tf_only_labels_simple(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["only_labels_simple"],
            expected_data=self.data["only_labels_simple_expected"],
            not_expected_data=self.data["only_labels_simple_not_expected"])

    def test_tf_only_labels_complex(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["only_labels_complex"],
            expected_data=self.data["only_labels_complex_expected"],
            not_expected_data=self.data["only_labels_complex_not_expected"])

    def test_tf_only_creator_1(self):
        self.make_login(self.logined_1)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_1_expected"],
            not_expected_data=self.data["self_tasks_1_not_expected"])

    def test_tf_only_creator_2(self):
        self.make_login(self.logined_2)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_2_expected"],
            not_expected_data=self.data["self_tasks_2_not_expected"])

    def test_tf_only_creator_3(self):
        self.make_login(self.logined_3)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["self_tasks"],
            expected_data=self.data["self_tasks_3_expected"],
            not_expected_data=self.data["self_tasks_3_not_expected"])

    def test_tf_complex_user_3_1(self):
        self.make_login(self.logined_3)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["complex_user_3_1"],
            expected_data=self.data["complex_user_3_1_expected"],
            not_expected_data=self.data["complex_user_3_1_not_expected"])

    def test_tf_complex_user_3_2(self):
        self.make_login(self.logined_3)
        self.url_get_data_test(
            self.filter_url, get_data=self.data["complex_user_3_2"],
            expected_data=self.data["complex_user_3_2_expected"],
            not_expected_data=self.data["complex_user_3_2_not_expected"])
