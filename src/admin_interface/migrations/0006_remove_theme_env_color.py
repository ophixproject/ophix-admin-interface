from django.db import migrations


class Migration(migrations.Migration):
    """Remove env_color fields from Theme — moved to ServerSettings in ophix-admin-settings."""

    dependencies = [
        ("admin_interface", "0005_theme_update_ophix_defaults"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="theme",
            name="env_color",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="env_color_dark_use",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="env_color_dark",
        ),
    ]
