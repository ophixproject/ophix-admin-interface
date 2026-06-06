from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add css_module_rounded_corners placeholder field.

    Uses ADD COLUMN IF NOT EXISTS so this migration is safe regardless of
    which version of 0047 a server previously applied:
      - Servers that ran 0047 without this field: column is added.
      - Servers that ran the short-lived 0047 that included this field: no-op.
      - Fresh installs: column is added after 0047's ten fields.
    """

    dependencies = [
        ("admin_interface", "0047_restore_legacy_fixture_fields"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE admin_interface_theme "
                        "ADD COLUMN IF NOT EXISTS `css_module_rounded_corners` "
                        "tinyint(1) NOT NULL DEFAULT 1"
                    ),
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="theme",
                    name="css_module_rounded_corners",
                    field=models.BooleanField(default=True),
                ),
            ],
        ),
    ]
