import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0003_theme_message_banner_colors"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_message_success_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#155724",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="success text",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_success_text_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_success_text_dark",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="dark",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_warning_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#856404",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="warning text",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_warning_text_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_warning_text_dark",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="dark",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_error_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#721c24",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="error text",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_error_text_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_error_text_dark",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="dark",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_info_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#0c5460",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="info text",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_info_text_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_info_text_dark",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="dark",
            ),
        ),
    ]
