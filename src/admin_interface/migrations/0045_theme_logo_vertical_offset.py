from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0044_theme_dark_mode_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="logo_vertical_offset",
            field=models.SmallIntegerField(
                default=0,
                verbose_name=_("vertical offset"),
                help_text=_("Pixels to shift the logo up (positive) or down (negative) relative to its natural position."),
            ),
        ),
    ]
