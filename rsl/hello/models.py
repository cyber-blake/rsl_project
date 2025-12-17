from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Article(models.Model):
    # Обязательные поля
    title = models.CharField(_("Заголовок"), max_length=200)
    slug = models.SlugField(_("Слаг"), max_length=200, unique=True)
    body = models.TextField(_("Текст статьи"))

    # Поле для главного изображения (обложки статьи)
    main_image = models.ImageField(
        _("Главное изображение"), upload_to="news_images", blank=True, null=True
    )

    pub_date = models.DateTimeField(_("Дата публикации"), auto_now_add=True)

    class Meta:
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель для хранения комментариев
    """

    commentText = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    approved = models.BooleanField(
        _("Одобрен"), default=False
    )  # todo отображать комментарии if approved:
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    email = models.EmailField(_("Эл. почта"), max_length=254)
    author = models.CharField(_("Автор комментария"), max_length=40)

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ["-pub_date"]

    def __str__(self):
        return f'Комментарий "{self.commentText}"'


# # --- Вариант для нескольких изображений (если нужно) ---
# class ArticleImage(models.Model):
#     article = models.ForeignKey(
#         Article,
#         on_delete=models.CASCADE,
#         related_name="images",
#         verbose_name=_("Статья"),
#     )
#     image = models.ImageField(_("Изображение"), upload_to="article_gallery/")
#     caption = models.CharField(_("Подпись"), max_length=255, blank=True)

#     class Meta:
#         verbose_name = _("Изображение статьи")
#         verbose_name_plural = _("Изображения статьи")
