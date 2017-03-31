from django.contrib.auth import (authenticate, get_user_model, login, logout, )
from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea, Comment

from .forms import UserLoginForm, UserRegisterForm, CommentForm, IdeaForm

User = get_user_model()


def index(request):
    return render(request, "main\index.html")


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/home")
    return render(request, "main\\login.html", {"form": form})


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/home")
    return render(request, "main\\register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def home(request):
    users = User.objects.all()
    ideas = Idea.objects.all().order_by('-timestamp')
    return render(request, "main\\home.html", {"users": users, "ideas": ideas})


def profile(request, username=None):
    person = get_object_or_404(User, username=username)
    ideas = Idea.objects.filter(user__username=username).order_by('-timestamp')
    comments = Comment.objects.filter(user__username=username).order_by('-timestamp')
    return render(request, "main\\profile.html", {"person": person, "ideas": ideas, "comments": comments})


def view_idea(request, idea_id=None):
    idea = get_object_or_404(Idea, id=idea_id)
    comments = Comment.objects.filter(idea__id=idea_id).order_by('-timestamp')
    form = CommentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.idea = idea
        instance.user = request.user
        instance.save()
    return render(request, "main\\view_idea.html", {"idea": idea, "comments": comments, "form": form})


def post_idea(request):
    form = IdeaForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("/home")
    return render(request, "main\\post_idea.html", {"form": form})




