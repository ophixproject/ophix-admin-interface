from django.db import migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0037_alter_theme_title_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_success_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#28A745",
                help_text="#28A745 — used for OK/healthy states in plugin dashboards",
                max_length=10,
                verbose_name="success / OK color",
            ),
        ),
    ]
