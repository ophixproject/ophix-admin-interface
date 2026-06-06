import admin_interface.models
from django.core.validators import FileExtensionValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0034_custom_css_vars_help_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="logo_dark",
            field=models.FileField(
                blank=True,
                help_text="Optional logo for dark mode. Shown when the OS/browser is in dark mode. Leave blank to use the standard logo in all modes.",
                upload_to=admin_interface.models._logo_dark_upload_to,
                validators=[
                    FileExtensionValidator(
                        allowed_extensions=["gif", "jpg", "jpeg", "png", "svg"]
                    )
                ],
                verbose_name="dark mode logo",
            ),
        ),
    ]
