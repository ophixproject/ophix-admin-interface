from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add css_module_rounded_corners placeholder field.

    This was omitted from 0047 and some installs already have 0047 applied
    without this column, so it is added here rather than modifying 0047.
    """

    dependencies = [
        ("admin_interface", "0047_restore_legacy_fixture_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="css_module_rounded_corners",
            field=models.BooleanField(default=True),
        ),
    ]
