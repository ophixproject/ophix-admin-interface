from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0036_remove_theme_logo_dark"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="title",
            field=models.CharField(
                blank=True,
                default="",
                max_length=50,
                verbose_name=_("title"),
            ),
        ),
    ]
