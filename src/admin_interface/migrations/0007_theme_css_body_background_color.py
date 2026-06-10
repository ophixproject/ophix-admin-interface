import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0006_remove_theme_env_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_body_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                help_text="Overall page background colour for all admin pages. Leave blank to use the browser default.",
                max_length=10,
                verbose_name="background color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_body_background_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_body_background_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
    ]
