"""Safely migrate hello.Article rows to Wagtail NewsPage.

Install as: hello/management/commands/migrate_articles_to_wagtail.py
Requires: NewsPage.legacy_article OneToOneField to hello.Article.

Run without arguments for a read-only preview, or --apply --backup-dir <path>
for a real migration. This command intentionally leaves old Article records intact.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.html import linebreaks
from wagtail.images import get_image_model
from wagtail.models import Page

from cms_news.models import NewsPage
from hello.models import Article, Comment


class Command(BaseCommand):
    help = "Move Django Articles to Wagtail NewsPages without deleting originals"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Actually create pages; otherwise preview without database writes",
        )
        parser.add_argument(
            "--backup-dir",
            help="Directory containing db.sqlite3 and a backed-up media directory",
        )

    def handle(self, *args, **options):
        if not hasattr(NewsPage, "legacy_article"):
            raise CommandError(
                "NewsPage.legacy_article is missing. Add the OneToOneField and migrate first."
            )

        root = Page.objects.filter(pk=2, slug="news").first()
        if root is None or root.get_parent() is None:
            raise CommandError("Could not find the Wagtail 'Новости' parent (id=2).")

        articles = list(Article.objects.select_related("image").order_by("pk"))
        pending = []
        problems = []
        total_comments = 0

        for article in articles:
            already = NewsPage.objects.filter(legacy_article_id=article.pk).first()
            if already is not None:
                self.stdout.write(
                    f"SKIP Article {article.pk}: already mapped to NewsPage {already.pk}"
                )
                continue

            sibling = Page.objects.child_of(root).filter(slug=article.slug).first()
            if sibling:
                problems.append(
                    f"Article {article.pk}: slug '{article.slug}' conflicts "
                    f"with existing Wagtail Page {sibling.pk}"
                )

            files = self.source_files(article)
            for role, field in files:
                try:
                    exists = field.storage.exists(field.name)
                except Exception as exc:
                    problems.append(f"Article {article.pk} / {role}: {exc}")
                    continue
                if not exists:
                    problems.append(
                        f"Article {article.pk} / {role}: file not found: {field.name}"
                    )

            count = Comment.objects.filter(article=article).count()
            total_comments += count
            self.stdout.write(
                f"Article {article.pk} -> /news/{article.slug}/ | "
                f"images={len(files)} | comments={count} | {article.title}"
            )
            pending.append(article)

        self.stdout.write(
            f"To transfer: {len(pending)} articles, "
            f"{total_comments} comments (their existing records will be retained)"
        )
        if problems:
            raise CommandError("Preflight failed:\n- " + "\n- ".join(problems))

        if not options["apply"]:
            self.stdout.write(self.style.SUCCESS("DRY RUN OK: database unchanged."))
            self.stdout.write("Run with --apply --backup-dir <backup-folder> after checking backups.")
            return

        backup_dir = options["backup_dir"]
        if not backup_dir:
            raise CommandError("--apply requires --backup-dir with a verified backup")
        backup_path = Path(backup_dir)
        if not (backup_path / "db.sqlite3").is_file():
            raise CommandError(f"Missing database backup: {backup_path / 'db.sqlite3'}")
        if not (backup_path / "media").is_dir():
            raise CommandError(f"Missing media backup: {backup_path / 'media'}")
        if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
            raise CommandError("Only the project's SQLite setup is supported")

        created = 0
        # Database changes are atomic; copied media files are not covered by DB rollback.
        with transaction.atomic():
            for article in pending:
                source_files = self.source_files(article)
                cover = None
                body_images = []
                for role, field in source_files:
                    image = self.copy_image(article, field, role)
                    if cover is None:
                        cover = image
                    else:
                        body_images.append(image)

                body = []
                if article.body:
                    # Original Django template used |linebreaks, which escapes raw HTML.
                    body.append(("paragraph", linebreaks(article.body)))
                for image in body_images:
                    body.append(("image", image))

                page = NewsPage(
                    title=article.title,
                    slug=article.slug,
                    body=body,
                    publication_date=article.pub_date,
                    main_image=cover,
                    legacy_article=article,
                    live=False,
                )
                root.add_child(instance=page)
                page.save_revision().publish()
                # Publishing sets timestamps to 'now'; retain the legacy publication date.
                Page.objects.filter(pk=page.pk).update(
                    first_published_at=article.pub_date,
                    last_published_at=article.pub_date,
                )

                changed = Comment.objects.filter(article=article).update(news_page=page)
                created += 1
                self.stdout.write(
                    f"CREATED NewsPage {page.pk} from Article {article.pk}; "
                    f"linked {changed} comments"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Done: created {created} NewsPages. No Article rows deleted.")
        )

    @staticmethod
    def source_files(article):
        """Prefer main_image as cover; preserve a separate original in body."""
        files = []
        if article.main_image and article.main_image.name:
            files.append(("main", article.main_image))
        if article.image_id and article.image.original and article.image.original.name:
            other = article.image.original
            if not files or files[0][1].name != other.name:
                files.append(("additional", other))
        return files

    @staticmethod
    def copy_image(article, source_field, role):
        image_model = get_image_model()
        original_basename = Path(source_field.name).name
        filename = f"legacy_{article.pk}_{role}_{original_basename}"
        # A fresh Wagtail media file is created; original source remains untouched.
        with source_field.open("rb") as stream:
            image = image_model(title=article.title[:255])
            image.file.save(filename, File(stream), save=True)
        return image
