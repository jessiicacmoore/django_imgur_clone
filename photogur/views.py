from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from photogur.models import Picture, Comment


def root(request):
    return HttpResponseRedirect('/pictures')

def pictures(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    picture_comments = Comment.objects.filter(picture=id)    

    context = {'picture': picture, 'comments': picture_comments}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)
    

def picture_search(request):
  query = request.GET['query']
  search_results = Picture.objects.filter(artist=query)
  context = {'pictures': search_results, 'query': query}
  response = render(request, 'search_results.html', context)
  return HttpResponse(response)