from django.db import migrations, models


def backfill_default_font_size(apps, schema_editor):
    Theme = apps.get_model("admin_interface", "Theme")
    Theme.objects.filter(css_body_font_size="").update(css_body_font_size="14px")


def noop_reverse(apps, schema_editor):
    # Deliberately not reverted -- there's no way to distinguish a row that was
    # blank before this migration from one an operator has since set to "14px"
    # on purpose, so reversing would risk clobbering a real choice.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0010_theme_css_disabled_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="css_body_font_size",
            field=models.CharField(
                blank=True,
                default="14px",
                help_text=(
                    "e.g. 14px · 0.875rem · Leave blank to fall back to the browser default."
                ),
                max_length=20,
                verbose_name="font size",
            ),
        ),
        migrations.RunPython(backfill_default_font_size, noop_reverse),
    ]
