import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0009_phase_e_notification_rename"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_disabled_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#666666",
                help_text="#666666 — used for disabled rows and records, distinct from ordinary muted/secondary text",
                max_length=10,
                verbose_name="disabled color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_disabled_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_disabled_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
    ]
