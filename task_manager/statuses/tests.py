from django.test import tag
from task_manager.tests.conftests import CustomTestCase
from task_manager.statuses.views import (
    StatusIndexView, StatusCreateView, StatusUpdateView, StatusDeleteView)


@tag("statuses")
class StatusesTestCase(CustomTestCase):
    data_json = 'statuses-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.status_logined = self.auth["status_logined"]
        self.delete_pk_task_used = self.data["delete_task_used"]["pk"]

# statuses_index tests:

    def test_statuses_unlogined(self):
        self.url_get_redirect_test(
            "statuses_index", None,
            "login", StatusIndexView.message_not_authenticated)

    def test_statuses_logined(self):
        self.make_login(self.status_logined)
        self.url_get_data_test(
            "statuses_index", expected_data=self.data["statuses_expected"])

# statuses_create tests:

    def test_status_create_unlogined(self):
        self.url_get_redirect_test(
            "statuses_create", None,
            "login", StatusCreateView.message_not_authenticated)

    def test_status_create_logined(self):
        self.make_login(self.status_logined)
        self.url_post_data_redirect_test(
            "statuses_create", None, self.data["create"],
            "statuses_index", StatusCreateView.success_message)
        self.url_get_data_test(
            "statuses_index", expected_data=self.data["create_expected"])

# statuses_update tests:

    def test_status_update_unlogined(self):
        self.url_get_redirect_test(
            "statuses_update", self.update_pk,
            "login", StatusUpdateView.message_not_authenticated)

    def test_status_update_logined(self):
        self.make_login(self.status_logined)
        self.url_get_test("statuses_update", self.update_pk)
        self.url_post_data_redirect_test(
            "statuses_update", self.update_pk, self.data["update"],
            "statuses_index", StatusUpdateView.success_message)
        self.url_get_data_test(
            "statuses_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# statuses_delete tests:

    def test_status_delete_unlogined(self):
        self.url_get_redirect_test(
            "statuses_delete", self.delete_pk,
            "login", StatusDeleteView.message_not_authenticated)

    def test_status_delete_logined_task_unused(self):
        self.make_login(self.status_logined)
        self.url_get_test("statuses_delete", self.delete_pk)
        self.url_post_data_redirect_test(
            "statuses_delete", self.delete_pk, self.data["delete"],
            "statuses_index", StatusDeleteView.success_message)
        self.url_get_data_test(
            "statuses_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_status_delete_logined_task_used(self):
        self.make_login(self.status_logined)
        self.url_get_test("statuses_delete", self.delete_pk_task_used)
        self.url_post_data_redirect_test(
            "statuses_delete", self.delete_pk_task_used, self.data["delete"],
            "statuses_index", StatusDeleteView.message_used_object)
        self.url_get_data_test(
            "statuses_index", expected_data=self.data["statuses_expected"])
