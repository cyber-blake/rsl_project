from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User
from cms_news.models import NewsPage


class Comment(models.Model):
    """Модель для хранения комментариев."""

    commentText = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    approved = models.BooleanField(_("Одобрен"), default=True)

    news_page = models.ForeignKey(
        NewsPage,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
        verbose_name="Новость Wagtail",
    )

    email = models.EmailField(_("Эл. почта"), max_length=254)

    author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="comments",
    max_length=40,
    )

    def can_edit(self, user):
        return user == self.author

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ["-pub_date"]

    def __str__(self):
        return f'Комментарий "{self.commentText}"'