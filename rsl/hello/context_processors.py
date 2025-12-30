from .models import Article


def latest_news(request):
    return {"latest_news_list": Article.objects.order_by("-pub_date")[:4]}
