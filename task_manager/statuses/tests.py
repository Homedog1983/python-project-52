from task_manager.tests.conftests import CustomTestCase
from django.urls import reverse
from task_manager.statuses.views import (
    StatusIndexView, StatusCreateView, StatusUpdateView, StatusDeleteView)


class StatusesTestCase(CustomTestCase):
    data_json = 'statuses-data.json'

    def setUp(self):
        super().setUp()
        self.update_pk = self.data["update"]["pk"]
        self.delete_pk = self.data["delete"]["pk"]
        self.user = self.auth["user"]

# statuses_index tests:

    def test_statuses_unlogined(self):
        response = self.client.get(
            reverse("statuses_index"), follow=True)
        self.redirect_with_message_test(
            response, "login", StatusIndexView.message_not_authenticated)

    def test_statuses_logined(self):
        self.make_login(self.user)
        self.url_data_test(
            "statuses_index", expected_data=self.data["statuses_expected"])

# statuses_create tests:

    def test_status_create_unlogined(self):
        response = self.client.get(
            reverse("statuses_create"), follow=True)
        self.redirect_with_message_test(
            response, "login", StatusCreateView.message_not_authenticated)

    def test_status_create_logined(self):
        self.make_login(self.user)
        response = self.client.post(
            reverse("statuses_create"), self.data["create"], follow=True)
        self.redirect_with_message_test(
            response, "statuses_index", StatusCreateView.message_success)
        self.url_data_test(
            "statuses_index", expected_data=self.data["create_expected"])

# statuses_update tests:

    def test_status_update_unlogined(self):
        response = self.client.get(
            reverse("statuses_update", args=[self.update_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", StatusUpdateView.message_not_authenticated)

    def test_status_update_logined(self):
        self.make_login(self.user)
        response = self.client.get(
            reverse("statuses_update", args=[self.update_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("statuses_update", args=[self.update_pk,]),
            self.data["update"],
            follow=True)
        self.redirect_with_message_test(
            response, "statuses_index", StatusUpdateView.message_success)
        self.url_data_test(
            "statuses_index",
            expected_data=self.data["update_expected"],
            not_expected_data=self.data["update_not_expected"])

# statuses_delete tests:

    def test_status_delete_unlogined(self):
        response = self.client.get(
            reverse("statuses_delete", args=[self.delete_pk,]),
            follow=True)
        self.redirect_with_message_test(
            response, "login", StatusDeleteView.message_not_authenticated)

    def test_status_delete_logined_task_unused(self):
        self.make_login(self.user)
        response = self.client.get(
            reverse("statuses_delete", args=[self.delete_pk,]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("statuses_delete", args=[self.delete_pk,]),
            self.data["delete"],
            follow=True)
        self.redirect_with_message_test(
            response, "statuses_index", StatusDeleteView.message_success)
        self.url_data_test(
            "statuses_index",
            expected_data=self.data["delete_expected"],
            not_expected_data=self.data["delete_not_expected"])

    def test_status_delete_logined_task_used(self):
        pass
        # self.make_login(self.user)
        # response = self.client.get(
        #     reverse("statuses_delete", args=[self.delete_pk,]))
        # self.assertEqual(response.status_code, 200)

        # response = self.client.post(
        #     reverse("statuses_delete", args=[self.delete_pk,]),
        #     self.data["delete"],
        #     follow=True)
        # self.redirect_with_message_test(
        #     response, "statuses_index", StatusDeleteView.message_success)
        # self.url_data_test(
        #     "statuses_index",
        #     expected_data=self.data["delete_expected"],
        #     not_expected_data=self.data["delete_not_expected"])
