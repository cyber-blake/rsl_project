from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock
from wagtail.admin.widgets import SlugInput

from .blocks import (
    EventDetailsBlock,
    PersonCardBlock,
    NoticeBlock,
    FAQBlock,
    ArticleMetaBlock,
)


class CarouselSlideBlock(blocks.StructBlock):
    image = ImageBlock(
        label="Изображение",
        required=True,
    )
    caption = blocks.CharBlock(
        label="Подпись",
        required=False,
    )

    class Meta:
        label = "Слайд"
        icon = "image"


class CarouselBlock(blocks.StructBlock):
    slides = blocks.ListBlock(
        CarouselSlideBlock(),
        label="Слайды",
        min_num=1,
    )

    class Meta:
        label = "Карусель изображений"
        icon = "image"
        template = "cms_news/blocks/carousel.html"



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

    legacy_article = models.OneToOneField(
        "hello.Article",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="wagtail_news_page",
        verbose_name="Исходная статья Django",
    )
    
    body = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    label="Текст",
                    template="cms_news/blocks/paragraph.html",
                ),
            ),
            (
                "heading",
                blocks.CharBlock(
                    label="Подзаголовок",
                    template="cms_news/blocks/heading.html",
                ),
            ),
            (
                "quote",
                blocks.BlockQuoteBlock(
                    label="Цитата",
                    template="cms_news/blocks/quote.html",
                ),
            ),
            (
                "image",
                ImageBlock(
                    label="Изображение",
                    required=False,
                ),
            ),

            (
                "carousel",
                CarouselBlock(),
            ),
            
            (
                "event_details",
                EventDetailsBlock(),
            ),
            (
                "person_card",
                PersonCardBlock(),
            ),
            (
                "notice",
                NoticeBlock(),
            ),
            (
                "faq",
                FAQBlock(),
            ),
            (
                "article_meta",
                ArticleMetaBlock(),
            ),


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
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["comments"] = (self.comments.filter(approved=True).select_related("author").order_by("-pub_date"))
        return context
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"