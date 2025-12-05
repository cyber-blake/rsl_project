from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Получаем модель пользователя, которая используется в проекте
User = get_user_model()


class Comment(models.Model):
    """
    Модель для хранения комментариев.
    Использует GenericForeignKey для привязки к любому объекту (статье, продукту и т.д.).
    """

    # 3. Текст комментария
    text = models.TextField(verbose_name="Текст комментария")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий f{self.text}"
