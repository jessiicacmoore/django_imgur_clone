from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm


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
    search_results = (
        Picture.objects.filter(title__icontains=query)
    ) | Picture.objects.filter(artist__icontains=query)
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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            pw = form.cleaned_data["password"]
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/pictures")
            else:
                form.add_error("username", "Login failed")
    else:
        form = LoginForm()

    context = {"form": form}
    http_response = render(request, "login.html", context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/pictures")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/pictures")
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def new_picture_view(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            form.save()
            return redirect("picture_details", id=instance.id)
    else:
        form = PictureForm()
            
    html_response = render(request, "new_picture.html", {'form': form})
    return HttpResponse(html_response)

@login_required
def edit_picture_view(request, id):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            form.save()
            return redirect("picture_details", id=instance.id)
    else:
        form = PictureForm()
    picture = Picture.objects.get(id=id)
    context = {'form': form, 'picture': picture}
    html_response = render(request, "edit_picture.html", context)
    return HttpResponse(html_response)