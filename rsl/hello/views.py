from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from .models import Comment, Article
from .forms import CommentForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cms_news.models import NewsPage
from django.contrib import messages
import re
from django.db.models.functions import Coalesce
from django.utils.html import strip_tags
from django.utils.text import Truncator

def index(request):
    # Получаем 5 последних опубликованных новостей Wagtail
    pages = (
        NewsPage.objects
        .live()
        .public()
        .annotate(
            sort_date=Coalesce(
                "publication_date",
                "first_published_at",
            )
        )
        .order_by("-sort_date")[:5]
    )

    latest_news = []

    for page in pages:
        paragraphs = []

        # Извлекаем текст из абзацев StreamField
        for block in page.body:
            if block.block_type == "paragraph":
                text = strip_tags(str(block.value)).strip()

                if text:
                    paragraphs.append(text)

        full_text = " ".join(paragraphs)

        # Первые два предложения
        sentences = re.split(r"(?<=[.!?])\s+", full_text)
        preview = " ".join(sentences[:2])

        # Не более 280 символов
        preview = Truncator(preview).chars(280)

        latest_news.append({
            "page": page,
            "preview": preview,
        })

    return render(
        request,
        "index.html",
        {
            "latest_news": latest_news,
        },
    )


# пробные 4 страницы с шаблонами оформления, пока пусть будут
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
    edit_id = request.GET.get("edit")
    edit_comment = None
    edit_form = None
    if edit_id:
        edit_comment = get_object_or_404(Comment, pk=edit_id)
        if request.user == edit_comment.author:
            edit_form = CommentEditForm(instance=edit_comment)
    context = {
        "article": article,
        "comments": comments_list,
        "form": form,
        "edit_comment": edit_comment,
        "edit_form": edit_form,
    }
    return render(request, "news_page.html", context)


# def get_latest_news(request):
#     latest_news_list = Article.objects.order_by("-pub_date")[:4]
#     context = {"latest_news_list": latest_news_list}
#     return render(request, "news_page.html", context)


def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                article=article,
                email=form.cleaned_data["email"],
                commentText=form.cleaned_data["commentText"],
                author=request.user,
            )
            # ✅ редирект ТОЛЬКО при успехе
            return redirect("news_page", pk=pk)

        comments_list = Comment.objects.filter(approved=True, article=article).order_by(
            "-pub_date"
        )

        return render(
            request,
            "news_page.html",
            {
                "article": article,
                "form": form,  # форма с ошибками
                "comments": comments_list,
            },
        )

    # защита от прямого GET-запроса
    return redirect("news_page", pk=pk)


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Удалять комментарий может только его автор
    if comment.author_id != request.user.id:
        return HttpResponseForbidden("Нельзя удалить чужой комментарий")

    # Определяем страницу для возврата
    if comment.news_page_id:
        redirect_url = comment.news_page.get_url(request=request)
    else:
        redirect_url = reverse("news_page", kwargs={"pk": comment.article_id})

    # Мягкое удаление
    comment.approved = False
    comment.save(update_fields=["approved"])

    return redirect(redirect_url)


@require_POST
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return JsonResponse(
            {"status": "error", "message": "Чужое править нельзя"}, status=403
        )

    new_text = request.POST.get("text")

    if new_text:
        comment.commentText = new_text
        comment.save()

        return JsonResponse(
            {
                "status": "ok",
                "text": comment.commentText,
            }
        )

    return JsonResponse({"status": "error", "message": "Пустой текст"}, status=400)


@login_required
def profile_view(request):
    comments = (
        Comment.objects
        .filter(author=request.user, approved=True)
        .select_related("article", "news_page")
        .order_by("-pub_date")
    )

    return render(
        request,
        "profile.html",
        {
            "user": request.user,
            "comments": comments,
        },
    )

@login_required
@require_POST
def add_wagtail_comment(request, pk):
    page = get_object_or_404(NewsPage, pk=pk, live=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        Comment.objects.create(
            news_page=page,
            author=request.user,
            email=form.cleaned_data["email"],
            commentText=form.cleaned_data["commentText"],
        )
    else:
        messages.error(request, "Проверьте заполнение формы комментария.")

    return redirect(page.get_url(request=request))