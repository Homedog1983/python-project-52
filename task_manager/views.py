# from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView


class IndexView(TemplateView):

    template_name = "index.html"
