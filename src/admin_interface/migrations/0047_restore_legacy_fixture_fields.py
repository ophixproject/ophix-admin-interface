from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Restore fields removed in 0041 as no-op placeholders so existing theme
    fixtures can be deserialized without errors.  Drop this migration (and the
    corresponding model fields) when migrations are squashed and all fixtures
    have been cleaned up.
    """

    dependencies = [
        ("admin_interface", "0046_theme_title_font_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="title",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AddField(
            model_name="theme",
            name="title_visible",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="theme",
            name="env_name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AddField(
            model_name="theme",
            name="env_visible_in_header",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="theme",
            name="env_visible_in_favicon",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="theme",
            name="language_chooser_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="theme",
            name="language_chooser_control",
            field=models.CharField(blank=True, default="minimal-select", max_length=100),
        ),
        migrations.AddField(
            model_name="theme",
            name="language_chooser_display",
            field=models.CharField(blank=True, default="name", max_length=100),
        ),
        migrations.AddField(
            model_name="theme",
            name="dark_mode_link_lightness",
            field=models.CharField(blank=True, default="70", max_length=20),
        ),
        migrations.AddField(
            model_name="theme",
            name="custom_css_vars",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_module_rounded_corners",
            field=models.BooleanField(default=True),
        ),
    ]
