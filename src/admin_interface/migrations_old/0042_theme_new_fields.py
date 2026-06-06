from django.db import migrations, models
import colorfield.fields


class Migration(migrations.Migration):
    """
    Add body text, button, border radius, and alert color fields to Theme.
    Replace css_module_rounded_corners (boolean) with css_module_border_radius (CharField).
    """

    dependencies = [
        ("admin_interface", "0041_remove_settings_fields"),
    ]

    operations = [
        # Replace boolean rounded corners with an actual radius value
        migrations.RemoveField(model_name="theme", name="css_module_rounded_corners"),
        migrations.AddField(
            model_name="theme",
            name="css_module_border_radius",
            field=models.CharField(
                blank=True,
                default="4px",
                help_text="e.g. 4px · 0px · 0.5rem",
                max_length=20,
                verbose_name="border radius",
            ),
        ),
        # Body text
        migrations.AddField(
            model_name="theme",
            name="css_body_font_family",
            field=models.CharField(
                blank=True,
                default="",
                help_text="e.g. Arial, sans-serif · Leave blank to use the browser default.",
                max_length=200,
                verbose_name="font family",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_body_font_size",
            field=models.CharField(
                blank=True,
                default="",
                help_text="e.g. 14px · 0.875rem · Leave blank to use the browser default.",
                max_length=20,
                verbose_name="font size",
            ),
        ),
        # Button
        migrations.AddField(
            model_name="theme",
            name="css_button_font_size",
            field=models.CharField(
                blank=True,
                default="",
                help_text="e.g. 13px · Leave blank to use the browser default (13px).",
                max_length=20,
                verbose_name="font size",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_button_border_radius",
            field=models.CharField(
                blank=True,
                default="",
                help_text="e.g. 4px · 50% · Leave blank for no rounding.",
                max_length=20,
                verbose_name="border radius",
            ),
        ),
        # Notification colors
        migrations.AddField(
            model_name="theme",
            name="css_alert_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#BA2121",
                help_text="#BA2121 — used for dangerous actions, error states, and alert buttons",
                max_length=10,
                verbose_name="alert / danger color",
            ),
        ),
    ]
