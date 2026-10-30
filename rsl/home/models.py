from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import CardsBlock, HeroBlock, LatestNewsBlock, PromoBlock, QuickLinksBlock


class HomePage(Page):
    """Контент главной страницы. Корень сайта и текущий маршрут / не меняем."""

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    sections = StreamField(
        [
            ("hero", HeroBlock()),
            ("cards", CardsBlock()),
            ("quick_links", QuickLinksBlock()),
            ("latest_news", LatestNewsBlock()),
            ("promo", PromoBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции главной страницы",
    )

    content_panels = Page.content_panels + [FieldPanel("sections")]
