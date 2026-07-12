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


def drop_columns_if_present(apps, schema_editor):
    """
    Drop each column only if it's actually present, via Django's own schema
    editor + introspection rather than backend-specific raw SQL (the previous
    RunSQL version used MySQL/MariaDB backtick-quoted identifiers, which are
    a syntax error on Postgres/Oracle/SQL Server/CockroachDB). Safe to run
    even if some or all columns were already dropped (e.g. when the
    django_migrations row was removed during the post-squash cleanup).
    """
    Theme = apps.get_model("admin_interface", "Theme")
    table_name = Theme._meta.db_table
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        existing = {
            col.name
            for col in connection.introspection.get_table_description(cursor, table_name)
        }
    for field_name in FIELDS:
        if field_name in existing:
            field = Theme._meta.get_field(field_name)
            schema_editor.remove_field(Theme, field)


class Migration(migrations.Migration):

    dependencies = [
        ("admin_interface", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(drop_columns_if_present, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.RemoveField(model_name="theme", name=f)
                for f in FIELDS
            ],
        ),
    ]
