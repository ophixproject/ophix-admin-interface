from django.db import migrations


FIELDS = [
    "title",
    "title_visible",
    "env_name",
    "env_visible_in_header",
    "env_visible_in_favicon",
    "language_chooser_active",
    "language_chooser_control",
    "language_chooser_display",
    "dark_mode_link_lightness",
    "custom_css_vars",
    "css_module_rounded_corners",
]

# Build a single ALTER TABLE with IF EXISTS for each column so the migration is
# safe to run even if some or all columns were already dropped (e.g. when the
# django_migrations row was removed during the post-squash cleanup).
_drop_sql = "ALTER TABLE `admin_interface_theme` " + ", ".join(
    f"DROP COLUMN IF EXISTS `{f}`" for f in FIELDS
)


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(_drop_sql, migrations.RunSQL.noop),
            ],
            state_operations=[
                migrations.RemoveField(model_name="theme", name=f)
                for f in FIELDS
            ],
        ),
    ]
