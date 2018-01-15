from django.http import HttpResponse
from django.shortcuts import render
# https://pypi.python.org/pypi/djangoajax
from django_ajax.decorators import ajax


def index(request):
    template_name = 'chartjs/index.html'
    context = {}
    return render(request, template_name, context)


def json(request):
    return HttpResponse("Test.")
# @ajax
# def my_view(request):
#     c = 2 + 3
#     return {'result': c}
