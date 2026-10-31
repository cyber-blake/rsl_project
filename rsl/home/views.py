from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render

from .models import HomePage


@staff_member_required(login_url="/cms/login/")
def home_preview(request):
    """Приватный просмотр новой главной без изменения действующего /."""
    page = HomePage.objects.live().first()
    if page is None:
        raise Http404("Опубликованная главная страница ещё не создана")
    return render(request, "home/home_page.html", {"page": page})

def homepage(request):
    page = HomePage.objects.live().public().first()

    if page is None:
        return render(request, "index.html")

    return render(request, "home/home_page.html", {"page": page})