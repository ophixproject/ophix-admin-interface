import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0007_theme_css_body_background_color"),
    ]

    operations = [
        # #43 tab border-radius
        migrations.AddField(
            model_name="theme",
            name="css_tab_border_radius",
            field=models.CharField(
                blank=True,
                default="0",
                help_text="e.g. 4px · 0px · 0.5rem. Controls tab and nav sidebar toggle handle border-radius independently of modules.",
                max_length=20,
                verbose_name="tab border radius",
            ),
        ),
        # #23 body text color
        migrations.AddField(
            model_name="theme",
            name="css_body_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                help_text="Body text colour. Leave blank to use the browser default.",
                max_length=10,
                verbose_name="text color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_body_text_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_body_text_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
        # #37 action button colors
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#888888",
                help_text="Background colour of capsule-shaped action buttons (History, Duplicate, etc.)",
                max_length=10,
                verbose_name="background color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_hover_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#747474",
                help_text="Action button background colour on hover",
                max_length=10,
                verbose_name="hover background",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_hover_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_background_hover_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_text_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="#FFFFFF",
                help_text="Text colour on action buttons",
                max_length=10,
                verbose_name="text color",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_text_color_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="css_action_button_text_color_dark",
            field=colorfield.fields.ColorField(blank=True, default="", max_length=10, verbose_name="dark"),
        ),
    ]
