import os
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile


class ImageService:

    @staticmethod
    def generate_versions(image_instance):
        original = image_instance.original
        img = PilImage.open(original).convert("RGB")

        base_path = os.path.dirname(original.name)

        # PREVIEW (до 1200px)
        preview = img.copy()
        preview.thumbnail((1200, 1200))
        preview_io = BytesIO()
        preview.save(preview_io, format="JPEG", quality=85)
        image_instance.preview.save(
            f"{base_path}/preview.jpg", ContentFile(preview_io.getvalue()), save=False
        )

        # THUMB (300px)
        thumb = img.copy()
        thumb.thumbnail((300, 300))
        thumb_io = BytesIO()
        thumb.save(thumb_io, format="JPEG", quality=80)
        image_instance.thumb.save(
            f"{base_path}/thumb.jpg", ContentFile(thumb_io.getvalue()), save=False
        )

        # WEBP
        webp_io = BytesIO()
        img.save(webp_io, format="WEBP", quality=80)
        image_instance.webp.save(
            f"{base_path}/image.webp", ContentFile(webp_io.getvalue()), save=False
        )
