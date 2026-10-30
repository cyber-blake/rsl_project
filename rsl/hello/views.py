from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from .models import Comment
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
from django.core.paginator import Paginator


def get_all_news(request):
    """Получает все опубликованные новости Wagtail."""

    news_list = []

    def make_preview(text):
        text = " ".join(strip_tags(text).split())
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return Truncator(" ".join(sentences[:2])).chars(220)

    pages = NewsPage.objects.live().public()

    for page in pages:
        paragraphs = []
        search_parts = [page.title]

        for block in page.body:
            if block.block_type in ("paragraph", "heading", "quote"):
                text = strip_tags(str(block.value))
                search_parts.append(text)

                if block.block_type == "paragraph":
                    paragraphs.append(text)

        full_text = " ".join(paragraphs)

        image_url = None

        if page.main_image:
            image_url = page.main_image.get_rendition(
                "fill-640x360"
            ).url

        news_list.append({
            "title": page.title,
            "date": (
                page.publication_date
                or page.first_published_at
                or page.last_published_at
            ),
            "preview": make_preview(full_text),
            "search_text": " ".join(search_parts).casefold(),
            "url": page.get_url(request=request),
            "image_url": image_url,
        })

    news_list.sort(
        key=lambda item: (
            item["date"].timestamp()
            if item["date"] else 0
        ),
        reverse=True,
    )

    return news_list


def index(request):
    latest_news = get_all_news(request)[:5]

    return render(
        request,
        "index.html",
        {"latest_news": latest_news},
    )



def news_page(request, pk):
    """Перенаправление старого ID новости на страницу Wagtail."""

    page = get_object_or_404(
        NewsPage.objects.live().public(),
        legacy_source_id=pk,
    )

    return redirect(page.get_url(request=request), permanent=True)


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Удалять комментарий может только его автор
    if comment.author_id != request.user.id:
        return HttpResponseForbidden("Нельзя удалить чужой комментарий")

    # Определяем страницу для возврата
    redirect_url = (
        comment.news_page.get_url(request=request)
        if comment.news_page_id
        else "/news/"
    )

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
        .select_related("news_page")
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



def news_archive(request):
    query = request.GET.get("q", "").strip()[:100]
    year_param = request.GET.get("year", "").strip()

    # Получаем все новости из двух моделей
    news = get_all_news(request)

    # Все доступные годы
    years = sorted(
        {
            item["date"].year
            for item in news
            if item["date"]
        },
        reverse=True,
    )

    selected_year = None

    if year_param.isdigit():
        year = int(year_param)

        if year in years:
            selected_year = year

    # Фильтрация по году
    if selected_year:
        news = [
            item for item in news
            if item["date"]
            and item["date"].year == selected_year
        ]

    # Поиск по заголовку и содержимому
    if query:
        terms = query.casefold().split()

        news = [
            item for item in news
            if all(
                term in item["search_text"]
                for term in terms
            )
        ]

    # Пагинация
    paginator = Paginator(news, 6)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "news_archive.html",
        {
            "news_cards": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
            "years": years,
            "selected_year": selected_year,
        },
    )

    query = request.GET.get("q", "").strip()[:100]
    year_param = request.GET.get("year", "").strip()

    news = (
        NewsPage.objects
        .live()
        .public()
        .annotate(
            sort_date=Coalesce(
                "publication_date",
                "first_published_at",
            )
        )
        .order_by("-sort_date", "-pk")
    )

    # Годы, за которые есть опубликованные новости
    years = sorted(
        {
            date.year
            for date in news.values_list("sort_date", flat=True)
            if date is not None
        },
        reverse=True,
    )

    # Фильтрация по году
    selected_year = None

    if len(year_param) == 4 and year_param.isdigit():
        selected_year = int(year_param)
        news = news.filter(sort_date__year=selected_year)

    # Поиск по заголовку и содержимому новости
    if query:
        terms = query.casefold().split()
        matched_news = []

        for page in news:
            text_parts = [page.title]

            for block in page.body:
                if block.block_type in (
                    "paragraph",
                    "heading",
                    "quote",
                ):
                    text_parts.append(
                        strip_tags(str(block.value))
                    )

            searchable_text = " ".join(text_parts).casefold()

            if all(term in searchable_text for term in terms):
                matched_news.append(page)

        news = matched_news

    # Пагинация по 6 новостей
    paginator = Paginator(news, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    news_cards = []

    for page in page_obj.object_list:
        paragraphs = []

        for block in page.body:
            if block.block_type == "paragraph":
                text = strip_tags(str(block.value)).strip()

                if text:
                    paragraphs.append(text)

        full_text = " ".join(paragraphs)
        sentences = re.split(r"(?<=[.!?])\s+", full_text)

        preview = Truncator(
            " ".join(sentences[:2])
        ).chars(220)

        news_cards.append({
            "page": page,
            "preview": preview,
        })

    return render(
        request,
        "news_archive.html",
        {
            "news_cards": news_cards,
            "page_obj": page_obj,
            "query": query,
            "years": years,
            "selected_year": selected_year,
        },
    )

    news = (
        NewsPage.objects
        .live()
        .public()
        .annotate(
            sort_date=Coalesce(
                "publication_date",
                "first_published_at",
            )
        )
        .order_by("-sort_date", "-pk")
    )

    paginator = Paginator(news, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    news_cards = []

    for page in page_obj.object_list:
        paragraphs = []

        for block in page.body:
            if block.block_type == "paragraph":
                text = strip_tags(str(block.value)).strip()

                if text:
                    paragraphs.append(text)

        full_text = " ".join(paragraphs)
        sentences = re.split(r"(?<=[.!?])\s+", full_text)

        preview = Truncator(
            " ".join(sentences[:2])
        ).chars(220)

        news_cards.append({
            "page": page,
            "preview": preview,
        })

    return render(
        request,
        "news_archive.html",
        {
            "news_cards": news_cards,
            "page_obj": page_obj,
        },
    )