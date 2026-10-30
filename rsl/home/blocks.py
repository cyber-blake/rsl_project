from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(label="Текст кнопки", max_length=90)
    url = blocks.CharBlock(
        label="Адрес ссылки",
        max_length=500,
        help_text="Например: /news/ или https://example.com/",
    )

    class Meta:
        label = "Ссылка"
        icon = "link"


class HeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(label="Надзаголовок", required=False, max_length=90)
    heading = blocks.CharBlock(label="Заголовок", max_length=180)
    description = blocks.TextBlock(label="Описание", required=False)
    image = ImageBlock(label="Изображение", required=False)
    buttons = blocks.ListBlock(LinkBlock(), label="Кнопки", required=False, max_num=4)
    theme = blocks.ChoiceBlock(
        label="Цвет фона",
        choices=[("sage", "Светло-зелёный"), ("cream", "Кремовый"), ("white", "Белый")],
        default="sage",
    )

    class Meta:
        label = "Главный баннер"
        icon = "image"
        template = "home/blocks/hero.html"


class ContentCardBlock(blocks.StructBlock):
    image = ImageBlock(label="Фото", required=False)
    title = blocks.CharBlock(label="Название", max_length=120)
    description = blocks.TextBlock(label="Описание", required=False)
    link_label = blocks.CharBlock(label="Текст ссылки", required=False, max_length=90)
    link_url = blocks.CharBlock(label="Адрес ссылки", required=False, max_length=500)

    class Meta:
        label = "Карточка"
        icon = "doc-full"


class CardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Название секции", required=False, max_length=180)
    cards = blocks.ListBlock(ContentCardBlock(), label="Карточки", min_num=1, max_num=6)

    class Meta:
        label = "Сетка карточек"
        icon = "grip"
        template = "home/blocks/cards.html"


class QuickLinksBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Название секции", required=False, max_length=180)
    links = blocks.ListBlock(LinkBlock(), label="Ссылки", min_num=1, max_num=10)

    class Meta:
        label = "Быстрые ссылки"
        icon = "link"
        template = "home/blocks/quick_links.html"


class LatestNewsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Название секции", default="Последние новости", max_length=180)
    count = blocks.IntegerBlock(label="Количество новостей", default=3, min_value=1, max_value=6)

    def get_context(self, value, parent_context=None):
        from django.db.models.functions import Coalesce
        from cms_news.models import NewsPage

        context = super().get_context(value, parent_context=parent_context)
        context["news_items"] = (
            NewsPage.objects.live().public()
            .annotate(home_sort_date=Coalesce("publication_date", "first_published_at"))
            .order_by("-home_sort_date", "-pk")[: value["count"]]
        )
        return context

    class Meta:
        label = "Последние новости (автоматически)"
        icon = "doc-full"
        template = "home/blocks/latest_news.html"


class PromoBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Заголовок", max_length=180)
    description = blocks.TextBlock(label="Описание", required=False)
    image = ImageBlock(label="Фото", required=False)
    link_label = blocks.CharBlock(label="Текст кнопки", required=False, max_length=90)
    link_url = blocks.CharBlock(label="Адрес кнопки", required=False, max_length=500)
    image_position = blocks.ChoiceBlock(
        label="Положение фотографии",
        choices=[("left", "Слева"), ("right", "Справа")],
        default="left",
    )

    class Meta:
        label = "Промоблок"
        icon = "image"
        template = "home/blocks/promo.html"
