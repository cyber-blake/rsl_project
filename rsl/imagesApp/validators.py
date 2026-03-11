from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(file):
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Некорректный файл изображения")


def validate_file_size(file):
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError("Максимальный размер 5MB")
