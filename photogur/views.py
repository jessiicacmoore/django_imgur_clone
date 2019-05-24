from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def pictures(request):
    response = render(request, 'index.html')
    return HttpResponse(response)