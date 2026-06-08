import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0002_remove_theme_placeholder_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_message_success_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#dff0d8",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="success background",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_success_bg_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_success_bg_dark",
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
            name="css_message_warning_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#fcf8e3",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="warning background",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_warning_bg_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_warning_bg_dark",
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
            name="css_message_error_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#f2dede",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="error background",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_error_bg_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_error_bg_dark",
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
            name="css_message_info_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#d9edf7",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="info background",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_info_bg_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_message_info_bg_dark",
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
