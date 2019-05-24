from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def pictures(request):
    response = render(request, 'pictures.html')
    return HttpResponse(response)