from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Comment, Article
from .forms import CommentForm
from django.urls import reverse
from .forms import CommentForm


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


# def comment_create(request, article_id):
#     # 1. Получаем статью, к которой пишем коммент
#     article = get_object_or_404(Article, id=article_id)

#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.article = article  # Автоматически заполняем связь
#             comment.save()
#             # Можно добавить сообщение об успехе (messages.success)
#             return redirect("article_detail", pk=article_id)
#     else:
#         form = CommentForm()

#     # 2. Получаем только те комментарии, что относятся к ЭТОЙ статье
#     comments = Comment.objects.filter(approved=True)

#     return render(
#         request,
#         "comments/comment_form.html",
#         {"form": form, "comments": comments, "article": article},
#     )


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            # Можно добавить сообщение об успехе (messages.success)
            return redirect("article_detail", pk=id)
    else:
        form = CommentForm()

    return render(request, "news_page.html", {"form": form})
