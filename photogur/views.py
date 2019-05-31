from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login


from photogur.models import Picture, Comment
from photogur.forms import LoginForm


def root(request):
    return HttpResponseRedirect("/pictures")


def pictures(request):
    context = {"pictures": Picture.objects.all()}
    response = render(request, "pictures.html", context)
    return HttpResponse(response)


def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    picture_comments = Comment.objects.filter(picture=id)

    context = {"picture": picture, "comments": picture_comments}
    response = render(request, "picture.html", context)
    return HttpResponse(response)


def picture_search(request):
    query = request.GET["query"]
    search_results = (Picture.objects.filter(title__icontains=query)) | Picture.objects.filter(artist__icontains=query)
    context = {"pictures": search_results, "query": query}
    response = render(request, "search_results.html", context)
    return HttpResponse(response)


@require_http_methods(["POST"])
def create_comment(request):
    user_name = request.POST["name"]
    user_message = request.POST["message"]
    user_picture = request.POST["picture"]
    Comment.objects.create(
        name=user_name,
        message=user_message,
        picture=Picture.objects.get(id=user_picture),
    )
    # Comment.objects.create(name=user_name, message=user_message, picture=user_picture)
    return redirect("picture_details", id=user_picture)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else: 
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = { 'form': form }
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)
