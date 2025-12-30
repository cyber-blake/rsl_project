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
    comments_list = Comment.objects.filter(approved=True, article=article).order_by(
        "-pub_date"
    )
    context = {"article": article, "comments": comments_list}
    return render(request, "news_page.html", context)


def get_latest_news(request):
    latest_news_list = Article.objects.order_by("-pub_date")[:4]
    context = {"latest_news_list": latest_news_list}
    return render(request, "news_page.html", context)


def add_comment(request, article_id):
    # 1. Находим пост в базе или выдаем 404, если его нет
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        # 2. Наполняем форму данными, которые прислал пользователь
        form = CommentForm(request.POST)

        # 3. Проверяем, всё ли заполнено корректно
        if form.is_valid():
            # 4. commit=False значит: "подготовь объект, но пока не сохраняй в базу"
            comment = form.save(commit=False)

            # 5. Привязываем комментарий к нашему посту
            comment.post = article

            # 6. Теперь сохраняем окончательно
            comment.save()

            # 7. Возвращаемся на страницу поста
            return redirect("news_page.html", pk=article.id)

    # Если метод GET (просто открыли страницу), форма будет пустой
    return redirect("news_page.html", pk=article.id)
