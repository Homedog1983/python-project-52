from django.test import tag
from task_manager.tests.conftests import BaseTestCase
from task_manager.labels.views import (
    LabelIndexView, LabelCreateView, LabelUpdateView, LabelDeleteView)


@tag("labels")
class StatusesTestCase(BaseTestCase):
    data_json = 'labels-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.logged = self.auth["labels_logged"]
        self.delete_pk_used_in_task = self.data["delete_used_in_task"]["pk"]

# labels_index tests:

    def test_get_labels_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "labels_index", None,
            "login", LabelIndexView.message_not_authenticated)

    def test_get_labels_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_response_data_after_get_request(
            "labels_index", expected_data=self.data["labels_expected"])

# labels_create tests:

    def test_get_labels_create_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "labels_create", None,
            "login", LabelCreateView.message_not_authenticated)

    def test_post_labels_create_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_redirect_with_message_after_post_request(
            "labels_create", None, self.data["create"],
            "labels_index", LabelCreateView.success_message)
        self.assert_response_data_after_get_request(
            "labels_index", expected_data=self.data["create_expected"])

# labels_update tests:

    def test_get_labels_update_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "labels_update", self.update_pk,
            "login", LabelUpdateView.message_not_authenticated)

    def test_dispatch_labels_update_by_logged(self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "labels_update", self.update_pk)
        self.assert_redirect_with_message_after_post_request(
            "labels_update", self.update_pk, self.data["update"],
            "labels_index", LabelUpdateView.success_message)
        self.assert_response_data_after_get_request(
            "labels_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# labels_delete tests:

    def test_get_labels_delete_by_unlogged(self):
        self.assert_redirect_with_message_after_get_request(
            "labels_delete", self.delete_pk,
            "login", LabelDeleteView.message_not_authenticated)

    def test_dispatch_labels_delete_by_logged_with_label_unused_in_task(
            self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "labels_delete", self.delete_pk)
        self.assert_redirect_with_message_after_post_request(
            "labels_delete", self.delete_pk, self.data["delete"],
            "labels_index", LabelDeleteView.success_message)
        self.assert_response_data_after_get_request(
            "labels_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_dispatch_labels_delete_by_logged_with_label_used_in_task(
            self):
        self.make_logged_as(self.logged)
        self.assert_status_code_after_get_request(
            "labels_delete", self.delete_pk_used_in_task)
        self.assert_redirect_with_message_after_post_request(
            "labels_delete",
            self.delete_pk_used_in_task, self.data["delete"],
            "labels_index", LabelDeleteView.message_used_object)
        self.assert_response_data_after_get_request(
            "labels_index", expected_data=self.data["labels_expected"])
