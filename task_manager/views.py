# from django.shortcuts import render
from django.views.generic.base import TemplateView
# from django.contrib.auth.models import User
# from django.utils.translation import gettext as _

class IndexView(TemplateView):

    template_name = "index.html"
