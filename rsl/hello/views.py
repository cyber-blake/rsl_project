from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Comment, Article
from .forms import CommentForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


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
    return render(request, "base.html", context)


@login_required
@require_POST
def add_comment(request, pk):
    """Добавление комментария."""
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        # Создаем объект, но не сохраняем в БД сразу, чтобы добавить автора и статью
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        return redirect("news_page", pk=pk)

    # Если форма невалидна, возвращаем ту же страницу с ошибками
    comments = article.comments.filter(approved=True).order_by("-pub_date")
    return render(
        request,
        "news_page.html",
        {
            "article": article,
            "form": form,
            "comments": comments,
        },
    )


@login_required
@require_POST
def delete_comment(request, pk):
    """Мягкое удаление (скрытие) комментария."""
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.approved = False
    comment.save(update_fields=["approved"])
    return redirect("news_page", pk=comment.article.pk)


@login_required
@require_POST
def edit_comment(request, pk):
    """AJAX редактирование комментария."""
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    new_text = request.POST.get("text", "").strip()

    if not new_text:
        return JsonResponse(
            {"status": "error", "message": "Текст не может быть пустым"}, status=400
        )

    comment.commentText = new_text
    comment.save(update_fields=["commentText"])

    return JsonResponse(
        {
            "status": "ok",
            "text": comment.commentText,
        }
    )
