from django.db import migrations


class Migration(migrations.Migration):
    """
    Remove fields that have moved to ophix-admin-settings (ServerSettings):
      title, title_visible, env_name, env_visible_in_header, env_visible_in_favicon,
      language_chooser_active, language_chooser_control, language_chooser_display.

    Also remove fields that are being retired entirely:
      dark_mode_link_lightness, custom_css_vars.
    """

    dependencies = [
        ("admin_interface", "0040_alter_theme_dark_mode_link_lightness_verbose_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="theme", name="title"),
        migrations.RemoveField(model_name="theme", name="title_visible"),
        migrations.RemoveField(model_name="theme", name="env_name"),
        migrations.RemoveField(model_name="theme", name="env_visible_in_header"),
        migrations.RemoveField(model_name="theme", name="env_visible_in_favicon"),
        migrations.RemoveField(model_name="theme", name="language_chooser_active"),
        migrations.RemoveField(model_name="theme", name="language_chooser_control"),
        migrations.RemoveField(model_name="theme", name="language_chooser_display"),
        migrations.RemoveField(model_name="theme", name="dark_mode_link_lightness"),
        migrations.RemoveField(model_name="theme", name="custom_css_vars"),
    ]
