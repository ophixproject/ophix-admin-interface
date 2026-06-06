from django.db import migrations, models

import admin_interface.validators


class Migration(migrations.Migration):
    dependencies = [
        ("admin_interface", "0033_ophix_extensions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="custom_css_vars",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text=(
                    'Additional CSS custom properties as a JSON object. '
                    'Keys must be valid CSS variable names starting with "--". '
                    'Example: {"--my-accent": "#c0392b", "--my-spacing": "8px"}. '
                    'Values must not contain ; { } or CSS functions (url, expression).'
                ),
                validators=[admin_interface.validators.validate_custom_css_vars],
                verbose_name="custom CSS variables",
            ),
        ),
    ]
