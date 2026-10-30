from django.core.management.base import BaseCommand
from wagtail.models import Page

from home.models import HomePage


class Command(BaseCommand):
    help = "Создать черновик главной страницы Wagtail отдельно от текущего корня сайта"

    def handle(self, *args, **options):
        page = HomePage.objects.first()
        if page:
            self.stdout.write(self.style.SUCCESS(f"HomePage уже существует: id={page.pk}. Откройте /cms/."))
            return

        root = Page.get_first_root_node()
        page = root.add_child(instance=HomePage(title="Главная страница", slug="home-page"))
        # Редактор наполнит секции и опубликует страницу через /cms/.
        self.stdout.write(self.style.SUCCESS(f"Создан черновик HomePage id={page.pk}. Заполните секции через /cms/."))
