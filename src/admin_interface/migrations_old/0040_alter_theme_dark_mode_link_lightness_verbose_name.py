from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0039_theme_dark_mode_link_lightness"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theme",
            name="dark_mode_link_lightness",
            field=models.CharField(
                choices=[
                    ("10", "10%"),
                    ("20", "20%"),
                    ("30", "30%"),
                    ("40", "40%"),
                    ("50", "50%"),
                    ("60", "60%"),
                    ("70", "70%"),
                    ("80", "80%"),
                ],
                default="30",
                help_text="How much white to mix into link and heading colours when dark mode is active. Increase for themes with darker accent colours.",
                max_length=2,
                verbose_name="accent lightness",
            ),
        ),
    ]
