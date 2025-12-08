from django.db import models


# Получаем модель пользователя, которая используется в проекте


class Comment(models.Model):
    """
    Модель для хранения комментариев
    """

    commentText = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField("date published", null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий {self.commentText}"
