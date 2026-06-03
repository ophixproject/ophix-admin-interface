from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0045_theme_logo_vertical_offset"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="title_font_size",
            field=models.CharField(
                max_length=20,
                blank=True,
                default="",
                help_text=_("e.g. 1.5rem, 24px · Leave blank to use the theme default."),
                verbose_name=_("font size"),
            ),
        ),
    ]
