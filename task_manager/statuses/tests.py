from django.test import tag
from task_manager.tests.conftests import BaseTestCase
from task_manager.statuses.views import (
    StatusIndexView, StatusCreateView, StatusUpdateView, StatusDeleteView)


@tag("statuses")
class StatusesTestCase(BaseTestCase):
    data_json = 'statuses-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.logged = self.auth["statuses_logged"]
        self.delete_pk_used_in_task = self.data["delete_used_in_task"]["pk"]

# statuses_index tests:

    def test_get_statuses_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "statuses_index", None,
            "login", StatusIndexView.message_not_authenticated)

    def test_get_statuses_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_response_data_after_get_request(
            "statuses_index", expected_data=self.data["statuses_expected"])

# statuses_create tests:

    def test_get_statuses_create_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "statuses_create", None,
            "login", StatusCreateView.message_not_authenticated)

    def test_post_statuses_create_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_redirect_with_message_after_post_request(
            "statuses_create", None, self.data["create"],
            "statuses_index", StatusCreateView.success_message)
        self.assert_response_data_after_get_request(
            "statuses_index", expected_data=self.data["create_expected"])

# statuses_update tests:

    def test_get_statuses_update_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "statuses_update", self.update_pk,
            "login", StatusUpdateView.message_not_authenticated)

    def test_dispatch_statuses_update_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "statuses_update", self.update_pk)
        self.assert_redirect_with_message_after_post_request(
            "statuses_update", self.update_pk, self.data["update"],
            "statuses_index", StatusUpdateView.success_message)
        self.assert_response_data_after_get_request(
            "statuses_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# statuses_delete tests:

    def test_get_statuses_delete_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "statuses_delete", self.delete_pk,
            "login", StatusDeleteView.message_not_authenticated)

    def test_dispatch_statuses_delete_by_logged_with_status_unused_in_task(
            self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "statuses_delete", self.delete_pk)
        self.assert_redirect_with_message_after_post_request(
            "statuses_delete", self.delete_pk, self.data["delete"],
            "statuses_index", StatusDeleteView.success_message)
        self.assert_response_data_after_get_request(
            "statuses_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_dispatch_statuses_delete_by_logged_with_status_used_in_task(
            self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "statuses_delete", self.delete_pk_used_in_task)
        self.assert_redirect_with_message_after_post_request(
            "statuses_delete",
            self.delete_pk_used_in_task, self.data["delete"],
            "statuses_index", StatusDeleteView.message_used_object)
        self.assert_response_data_after_get_request(
            "statuses_index", expected_data=self.data["statuses_expected"])
