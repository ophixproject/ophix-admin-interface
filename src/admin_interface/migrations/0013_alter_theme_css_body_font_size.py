from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0012_theme_related_modal_opacity_dark"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="css_body_font_size",
            field=models.CharField(
                blank=True,
                default="14px",
                help_text=(
                    "e.g. 14px · 0.875rem · Leave blank to fall back to the "
                    "browser default, which varies inconsistently page to page."
                ),
                max_length=20,
                verbose_name="font size",
            ),
        ),
    ]
