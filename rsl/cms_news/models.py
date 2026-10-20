from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock
from wagtail.admin.widgets import SlugInput


class NewsPage(Page):
    publication_date = models.DateTimeField(
        "Дата публикации",
        blank=True,
        null=True,
    )

    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        verbose_name="Обложка",
    )

    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(label="Текст")),
            ("heading", blocks.CharBlock(label="Подзаголовок")),
            ("quote", blocks.BlockQuoteBlock(label="Цитата")),
            ("image", ImageBlock(label="Изображение", required=False)),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Содержание",
    )

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("main_image"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
    FieldPanel("slug", widget=SlugInput(locale="ru")),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"