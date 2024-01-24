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
        self.label_logined = self.auth["label_logined"]
        self.delete_pk_task_used = self.data["delete_task_used"]["pk"]

# labels_index tests:

    def test_labels_unlogined(self):
        self.url_get_redirect_test(
            "labels_index", None,
            "login", LabelIndexView.message_not_authenticated)

    def test_labels_logined(self):
        self.make_login(self.label_logined)
        self.url_get_data_test(
            "labels_index", expected_data=self.data["labels_expected"])

# labels_create tests:

    def test_label_create_unlogined(self):
        self.url_get_redirect_test(
            "labels_create", None,
            "login", LabelCreateView.message_not_authenticated)

    def test_label_create_logined(self):
        self.make_login(self.label_logined)
        self.url_post_data_redirect_test(
            "labels_create", None, self.data["create"],
            "labels_index", LabelCreateView.success_message)
        self.url_get_data_test(
            "labels_index", expected_data=self.data["create_expected"])

# labels_update tests:

    def test_label_update_unlogined(self):
        self.url_get_redirect_test(
            "labels_update", self.update_pk,
            "login", LabelUpdateView.message_not_authenticated)

    def test_label_update_logined(self):
        self.make_login(self.label_logined)
        self.url_get_test("labels_update", self.update_pk)
        self.url_post_data_redirect_test(
            "labels_update", self.update_pk, self.data["update"],
            "labels_index", LabelUpdateView.success_message)
        self.url_get_data_test(
            "labels_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# labels_delete tests:

    def test_label_delete_unlogined(self):
        self.url_get_redirect_test(
            "labels_delete", self.delete_pk,
            "login", LabelDeleteView.message_not_authenticated)

    def test_label_delete_logined_task_unused(self):
        self.make_login(self.label_logined)
        self.url_get_test("labels_delete", self.delete_pk)
        self.url_post_data_redirect_test(
            "labels_delete", self.delete_pk, self.data["delete"],
            "labels_index", LabelDeleteView.success_message)
        self.url_get_data_test(
            "labels_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_label_delete_logined_task_used(self):
        self.make_login(self.label_logined)
        self.url_get_test("labels_delete", self.delete_pk_task_used)
        self.url_post_data_redirect_test(
            "labels_delete", self.delete_pk_task_used, self.data["delete"],
            "labels_index", LabelDeleteView.message_used_object)
        self.url_get_data_test(
            "labels_index", expected_data=self.data["labels_expected"])
