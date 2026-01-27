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


def news_page(request, pk):
    form = CommentForm()
    article = get_object_or_404(Article, pk=pk)
    comments_list = Comment.objects.filter(approved=True, article=article).order_by(
        "-pub_date"
    )
    context = {
        "article": article,
        "comments": comments_list,
        "form": form,
    }
    return render(request, "news_page.html", context)


def get_latest_news(request):
    latest_news_list = Article.objects.order_by("-pub_date")[:4]
    context = {"latest_news_list": latest_news_list}
    return render(request, "news_page.html", context)


def add_comment(request, pk):  # снести найух функцию
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        print("VALID:", form.is_valid())
        print("ERRORS:", form.errors)
        if form.is_valid():
            Comment.objects.create(
                article=article,
                email=form.cleaned_data["email"],
                commentText=form.cleaned_data["commentText"],
                author=form.cleaned_data["author"],
                # author=request.user if request.user.is_authenticated else None,
            )
            return redirect(request.path)
        else:
            comments_list = Comment.objects.filter(
                approved=True, article=article
            ).order_by("-pub_date")
            # Если форма НЕ валидна, мы НЕ должны делать редирект!
            # Мы должны отрендерить страницу статьи заново и передать туда форму с ошибками.
            context = {
                "article": article,
                "form": form,
                "comments": comments_list,
            }
            return redirect(request.path)

    return redirect("news_page.html", pk=pk)
