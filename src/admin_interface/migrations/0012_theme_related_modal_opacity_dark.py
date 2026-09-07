from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0011_theme_css_body_font_size_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="related_modal_background_opacity_dark_use",
            field=models.BooleanField(default=False, verbose_name="dark?"),
        ),
        migrations.AddField(
            model_name="theme",
            name="related_modal_background_opacity_dark",
            field=models.CharField(
                blank=True,
                choices=[
                    ("0.1", "10%"),
                    ("0.2", "20%"),
                    ("0.3", "30%"),
                    ("0.4", "40%"),
                    ("0.5", "50%"),
                    ("0.6", "60%"),
                    ("0.7", "70%"),
                    ("0.8", "80%"),
                    ("0.9", "90%"),
                ],
                default="0.3",
                max_length=5,
                verbose_name="dark",
            ),
        ),
    ]
