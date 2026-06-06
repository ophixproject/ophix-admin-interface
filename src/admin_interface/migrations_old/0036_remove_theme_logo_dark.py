from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0035_theme_logo_dark"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="theme",
            name="logo_dark",
        ),
    ]
