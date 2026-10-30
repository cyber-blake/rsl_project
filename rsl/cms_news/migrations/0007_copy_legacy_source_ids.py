from django.db import migrations
from django.db.models import F


def copy_legacy_ids(apps, schema_editor):
    NewsPage = apps.get_model("cms_news", "NewsPage")

    NewsPage.objects.filter(
        legacy_article_id__isnull=False
    ).update(
        legacy_source_id=F("legacy_article_id")
    )


class Migration(migrations.Migration):

    dependencies = [
        ("cms_news", "0006_newspage_legacy_source_id"),
    ]

    operations = [
        migrations.RunPython(
            copy_legacy_ids,
            migrations.RunPython.noop,
        ),
    ]