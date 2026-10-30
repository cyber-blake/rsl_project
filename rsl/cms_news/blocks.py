"""Reusable content blocks for Wagtail news pages."""

from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class EventDetailsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Заголовок", default="Детали мероприятия")
    event_date = blocks.DateBlock(label="Дата", required=True)
    start_time = blocks.TimeBlock(label="Время начала", required=False)
    end_time = blocks.TimeBlock(label="Время окончания", required=False)
    place = blocks.CharBlock(label="Место", required=False)
    admission = blocks.CharBlock(label="Вход", required=False)
    registration = blocks.CharBlock(label="Регистрация", required=False)
    contact = blocks.CharBlock(label="Контакт", required=False)

    class Meta:
        label = "Детали мероприятия"
        icon = "date"
        template = "cms_news/blocks/event_details.html"


class PersonCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Заголовок", default="Об авторе")
    name = blocks.CharBlock(label="Имя человека", required=False)
    photo = ImageBlock(label="Фотография", required=False)
    biography = blocks.RichTextBlock(label="Биография / описание", required=True)

    class Meta:
        label = "Карточка человека"
        icon = "user"
        template = "cms_news/blocks/person_card.html"


class NoticeBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        label="Тип сообщения",
        choices=[
            ("warning", "Предупреждение (жёлтый)"),
            ("info", "Информация (синий)"),
            ("success", "Хорошая новость (зелёный)"),
        ],
        default="warning",
    )
    heading = blocks.CharBlock(label="Заголовок")
    content = blocks.RichTextBlock(label="Текст сообщения")

    class Meta:
        label = "Важное сообщение"
        icon = "warning"
        template = "cms_news/blocks/notice.html"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(label="Вопрос")
    answer = blocks.RichTextBlock(label="Ответ")

    class Meta:
        label = "Вопрос и ответ"
        icon = "help"


class FAQBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Заголовок", default="Часто задаваемые вопросы")
    questions = blocks.ListBlock(FAQItemBlock(), label="Вопросы", min_num=1)

    class Meta:
        label = "FAQ — раскрывающиеся вопросы"
        icon = "help"
        template = "cms_news/blocks/faq.html"


class ArticleMetaBlock(blocks.StructBlock):
    author = blocks.CharBlock(label="Автор", required=False)
    reading_minutes = blocks.IntegerBlock(
        label="Время чтения, минут", required=False, min_value=1
    )
    tags = blocks.ListBlock(
        blocks.CharBlock(label="Тег", max_length=60),
        label="Теги",
        required=False,
    )

    class Meta:
        label = "Автор, время чтения и теги"
        icon = "tag"
        template = "cms_news/blocks/article_meta.html"
