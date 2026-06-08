from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0001_initial"),
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
        migrations.RemoveField(model_name="theme", name="css_module_rounded_corners"),
    ]
