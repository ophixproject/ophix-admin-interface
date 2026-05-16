import colorfield.fields
import admin_interface.models
import admin_interface.validators
from django.core.validators import FileExtensionValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_interface", "0032_alter_theme_defaults"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_warning_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#E67E22",
                help_text="#E67E22 — used for paused items, warnings, and amber UI states",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="warning / paused color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_muted_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#999999",
                help_text="#999999 — used for disabled items, secondary text, and muted UI states",
                image_field=None,
                max_length=10,
                samples=None,
                verbose_name="muted / disabled color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="custom_css_vars",
            field=models.JSONField(
                blank=True,
                default=dict,
                validators=[admin_interface.validators.validate_custom_css_vars],
                verbose_name="custom CSS variables",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Leave blank to use the default Django logo",
                upload_to=admin_interface.models._logo_upload_to,
                validators=[
                    FileExtensionValidator(
                        allowed_extensions=["gif", "jpg", "jpeg", "png", "svg"]
                    )
                ],
                verbose_name="logo",
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="favicon",
            field=models.FileField(
                blank=True,
                help_text="(.ico|.png|.gif - 16x16|32x32 px)",
                upload_to=admin_interface.models._favicon_upload_to,
                validators=[
                    FileExtensionValidator(
                        allowed_extensions=["gif", "ico", "jpg", "jpeg", "png", "svg"]
                    )
                ],
                verbose_name="favicon",
            ),
        ),
    ]
