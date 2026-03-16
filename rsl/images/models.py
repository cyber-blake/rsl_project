import uuid
from django.db import models
from django.utils import timezone
from .validators import validate_image, validate_file_size
from .services import ImageService
import shutil
from django.conf import settings


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    now = timezone.now()

    if not instance.uuid:
        instance.uuid = uuid.uuid4()

    return f"uploads/{now.year}/{now.month:02d}/" f"{instance.uuid}/original.{ext}"


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    original = models.ImageField(
        upload_to=upload_to, validators=[validate_image, validate_file_size]
    )

    preview = models.ImageField(blank=True)
    thumb = models.ImageField(blank=True)
    webp = models.ImageField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.uuid}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and self.original:
            ImageService.generate_versions(self)
            super().save(update_fields=["preview", "thumb", "webp"])


def delete(self, *args, **kwargs):
    folder_path = os.path.join(settings.MEDIA_ROOT, os.path.dirname(self.original.name))
    super().delete(*args, **kwargs)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
