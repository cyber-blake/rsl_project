
from cms_news.models import NewsPage
from django.db.models.functions import Coalesce


def latest_news(request):
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
        .order_by("-sort_date", "-pk")[:4]
    )

    return {"latest_news_list": news}
