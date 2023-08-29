from django.shortcuts import render, redirect
from encyclopedia.util import *
from django import forms
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
import markdown2
from random import randrange
import os
import re
from uuid import *
from encyclopedia.models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
import datetime

# Create your views here.
def index(request: HttpRequest):
    return render(request, "encyclopedia/index.html", {"posts": Article.objects.all(), "Classification": Classification.objects.all()})

def about(request: HttpRequest):
    return render(request, "encyclopedia/about.html",{"Classification": Classification.objects.all()})

@login_required(login_url='/login')
def article_view(request: HttpRequest, articleID: UUID):
    if request.method == "GET":
        liked = False
        try:
            lk = LikedArticle.objects.get(liker=request.user, article=Article.objects.get(article_id=articleID))
            liked = True
        except LikedArticle.DoesNotExist:
            liked = False
        return render(
            request,
            "encyclopedia/page.html",
            {
                "site": Article.objects.get(article_id=articleID),
                "content": markdown2.markdown(Article.objects.get(article_id=articleID).textual_content),
                "posts": Article.objects.all()[0:5],
                "Classification": Classification.objects.all(),
                "liked":liked,
                "like_count":LikedArticle.objects.filter(article=Article.objects.get(article_id=articleID)).count(),
                "comments":ArticleComment.objects.filter(article=Article.objects.get(article_id=articleID))
            }
        )
@login_required(login_url='/login')
def search_result(request: HttpRequest):
    if request.method == "POST":
        result = []
        searchKey = request.POST["q"]
        t = Article.objects.all()
        for x in t:
            if searchKey in x.title:
                result.append(x)
            else:
                continue
        return render(request, "encyclopedia/searched.html", {"results":result,"Classification": Classification.objects.all(), "searched":searchKey})
    else:
        return render(request, "encyclopedia/search.html")

@login_required(login_url="/login")
def author_page(request: HttpRequest, AuthorName: str):
    if request.method == "GET":
        author_info = Author.objects.get(name=AuthorName)
        t = Article.objects.filter(author=author_info)
        return render(request, "encyclopedia/author.html",{"posts":t, "User":author_info, "Classification": Classification.objects.all()})


@login_required(login_url='/login')
def random_result(request: HttpRequest):
    if request.method == "GET":
        t = Article.objects.all()
        if t.count() < 1:
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        index = random.randint(0, len(t)-1)
        return HttpResponseRedirect(reverse("encyclopedia:article", args=[t[index].article_id]))


@login_required(login_url='/login')
def classification_view(request: HttpRequest, classif: str):
    if request.method == "GET":
        classi = Classification.objects.get(name=classif)
        art = Article.objects.filter(article_classification=classi)
        return render(request, "encyclopedia/index.html", {"posts": art, "Classification": Classification.objects.all(), "classification": classif, "count":art.count()})

@login_required(login_url='/login')
def featured_view(request: HttpRequest):
    if request.method == "GET":
        art = Article.objects.filter(featured=True)
        return render(request, "encyclopedia/index.html", {"posts": art, "Classification": Classification.objects.all(), "count":art.count()})

@login_required(login_url='/login')
def liked_view(request: HttpRequest):
    if request.method == "GET":
        t = LikedArticle.objects.filter(liker=request.user)
        art = []
        for x in t:
            art.append(x.article)
        return render(request, "encyclopedia/likedArticles.html", {"posts": art, "Classification": Classification.objects.all()})

@login_required(login_url='/login')
def comment_view(request: HttpRequest, articleID: UUID):
    article = Article.objects.get(article_id=articleID)
    if request.method == "POST":
        try:
            new_comment = ArticleComment(
                commentid=uuid4(),
                commenter=request.user,
                article=article,
                comment_content=request.POST["commentContent"],
                date_commented=datetime.datetime.now()
            )
            new_comment.save()
            return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))
        except Exception:
            return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))

@login_required(login_url='/login')
def del_comment(request: HttpRequest, commentID: UUID, articleID: UUID):
    if request.method == "GET":
        comm = ArticleComment.objects.get(commentid=commentID)
        if comm.commenter == request.user:
            comm.delete()
            return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))
        else:
            return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))

@login_required(login_url='/login')      
def edit_comment(request: HttpRequest, commentID: UUID, articleID: UUID):
    if request.method == "POST":
        comm = ArticleComment.objects.get(commentid=commentID)
        if comm.commenter == request.user:
            comm.comment_content = request.POST["commentContent"]
            comm.date_commented = datetime.datetime.now()
            comm.save()
            return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))
    else:
        return HttpResponseRedirect(reverse("encyclopedia:article", kwargs={"articleID": articleID}))



@login_required(login_url='/login')
def like(request: HttpRequest, articleID: UUID):
    us = request.user
    article = Article.objects.get(article_id=articleID)
    if request.method == "GET":
        try:
            like = LikedArticle.objects.get(article=article, liker=us)
            like.delete()
        except LikedArticle.DoesNotExist:
            like = LikedArticle(article=article, liker=us)
            like.save()
        return HttpResponseRedirect(reverse("encyclopedia:article", args=[articleID]))
        


def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "encyclopedia/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            us = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "encyclopedia/login.html", {"error": "User does not exist"})
        au = authenticate(username=username, password=password)
        if au is not None:
            login(request,us)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/login.html", {"error": "Incorrect Username or Password"})


def register_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "encyclopedia/register.html")
    else:
        fname = request.POST["Fname"]
        lname = request.POST["Lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        cPassword = request.POST["c_password"]
        if password == cPassword:
            l = User(username=username, email=email, password=password, first_name=fname, last_name=lname)
            l.save()
            login(request,l)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/register.html", {"error": "Passwords do not match"})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("encyclopedia:index"))




    
