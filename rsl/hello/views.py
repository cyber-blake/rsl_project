from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Comment, Article


def index(request):
    return render(request, "index.html")


def news_one(request):
    """Отображает шаблон news-1.html"""
    return render(request, "news-1.html")


def news_two(request):
    """Отображает шаблон news-2.html"""
    return render(request, "news-2.html")


def news_three(request):
    """Отображает шаблон news-3.html"""
    return render(request, "news-3.html")


def news_four(request):
    """Отображает шаблон news-4.html"""
    return render(request, "news-4.html")


def news_page(request, id):
    article = get_object_or_404(Article, id=id)
    comments_list = Comment.objects.filter(article=article).order_by("pub_date")
    context = {"article": article, "comments": comments_list}
    return render(request, "news_page.html", context)
