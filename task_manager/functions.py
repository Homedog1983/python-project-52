from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import rollbar


def redirect_with_warning_message(
        request, warning_message, redirect_url_name):
    messages.warning(request, warning_message)
    return redirect(reverse(redirect_url_name))


def redirect_with_send_report_and_warning_message(
        rollbar_report_message, request, flash_message,
        redirect_url_name, report_type='fatal'):
    rollbar.report_message(rollbar_report_message, report_type)
    return redirect_with_warning_message(
        request, flash_message, redirect_url_name)
