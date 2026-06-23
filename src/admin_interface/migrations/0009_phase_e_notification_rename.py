import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):
    """Update help_text: 'system message banners' → 'system notifications' (Phase E naming #9)."""

    dependencies = [
        ("admin_interface", "0008_phase_c_theme_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="css_message_success_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#dff2e3",
                help_text="Background colour of success (green) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="success background",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_success_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#1a5c2b",
                help_text="Text colour of success (green) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="success text",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_warning_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#faf3e5",
                help_text="Background colour of warning (amber) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="warning background",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_warning_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#7a5000",
                help_text="Text colour of warning (amber) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="warning text",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_error_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#f5dede",
                help_text="Background colour of error (red) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="error background",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_error_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#6b0f0f",
                help_text="Text colour of error (red) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="error text",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_info_bg",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#d9f0f7",
                help_text="Background colour of info (cyan) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="info background",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="css_message_info_text",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#004d66",
                help_text="Text colour of info (cyan) system notifications",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="info text",
            ),
        ),
    ]
