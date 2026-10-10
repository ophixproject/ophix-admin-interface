"""
ophix-manage import_themes
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import Theme field values from a JSON file produced by export_themes.

Idempotent: themes are matched by name. Existing themes are updated only
when a field value differs; identical records are skipped.

`active` is deliberately never touched by this command, on create or
update — a save with `active=True` force-deactivates every other theme
(see Theme's own post_save signal), so importing historical data must
never silently change which theme is live on this server. A newly created
theme always comes back inactive; activate it explicitly afterward (admin,
or `ophix-manage set_theme`) if that's actually wanted.

`logo`/`favicon` are restored as plain path strings, same as every other
field — this command never recreates the actual image file. A server
missing the referenced media file behaves exactly as it already does for
any other broken/missing theme asset.

Examples
--------
Import every theme in the file:
    ophix-manage import_themes --input-file themes.json

Import a single theme by name:
    ophix-manage import_themes --input-file themes.json --name Midnight

Preview without writing:
    ophix-manage import_themes --input-file themes.json --dry-run
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

# Never part of a restore — see module docstring.
_EXCLUDED_FIELDS = frozenset({"active"})


class Command(BaseCommand):
    help = "Import Theme field values from a JSON file produced by export_themes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--input-file",
            required=True,
            metavar="FILE",
            help="Source file path (JSON produced by export_themes).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created or updated without making any changes.",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress per-record output. Summary line is always shown.",
        )
        parser.add_argument(
            "--name",
            metavar="NAME",
            action="append",
            dest="names",
            default=None,
            help="Only import theme(s) with this name. Repeat to specify multiple names.",
        )

    def handle(self, *args, **options):
        from django.apps import apps

        Theme = apps.get_model("admin_interface", "Theme")

        input_path = Path(options["input_file"])
        dry_run    = options["dry_run"]
        quiet      = options["quiet"]
        names      = options["names"]

        if not input_path.exists():
            raise CommandError(f"Input file not found: {input_path}")

        try:
            payload = json.loads(input_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON in {input_path}: {exc}")

        if not isinstance(payload, dict) or "themes" not in payload:
            raise CommandError("Unrecognised file format — expected export_themes output.")

        records = payload["themes"]
        if not isinstance(records, list):
            raise CommandError("Expected 'themes' to be a JSON array.")

        if names:
            names_set = set(names)
            records = [r for r in records if (r.get("name") or "").strip() in names_set]
            if not records:
                raise CommandError(
                    f"No records found matching --name filter: {', '.join(sorted(names_set))}"
                )

        created = updated = unchanged = skipped = 0

        for i, rec in enumerate(records, 1):
            name = (rec.get("name") or "").strip()
            if not name:
                self.stderr.write(f"  Record {i}: missing 'name' — skipped.")
                skipped += 1
                continue

            fields = {k: v for k, v in rec.items() if k != "name" and k not in _EXCLUDED_FIELDS}

            try:
                theme = Theme.objects.get(name=name)
                changed = {f: v for f, v in fields.items() if getattr(theme, f, None) != v}

                if not changed:
                    unchanged += 1
                    if not quiet:
                        self.stdout.write(f"  {name}: unchanged.")
                else:
                    if not quiet:
                        self.stdout.write(f"  {name}: updating {len(changed)} field(s).")
                    if not dry_run:
                        try:
                            for f, v in changed.items():
                                setattr(theme, f, v)
                            theme.full_clean()
                            theme.save()
                        except Exception as exc:
                            self.stderr.write(f"  {name}: save failed — {exc}")
                            skipped += 1
                            continue
                    updated += 1

            except Theme.DoesNotExist:
                if not quiet:
                    self.stdout.write(f"  {name}: creating.")
                if not dry_run:
                    try:
                        # active is never read from the file (see
                        # _EXCLUDED_FIELDS) — explicitly forced False here
                        # too, since Theme.active's own model default is
                        # True, which would otherwise silently deactivate
                        # every other theme on this server via Theme's own
                        # post_save signal the moment this save() runs.
                        theme = Theme(name=name, active=False, **fields)
                        theme.full_clean()
                        theme.save()
                    except Exception as exc:
                        self.stderr.write(f"  {name}: save failed — {exc}")
                        skipped += 1
                        continue
                created += 1

        parts = []
        if created:
            parts.append(f"{created} created")
        if updated:
            parts.append(f"{updated} updated")
        if unchanged:
            parts.append(f"{unchanged} unchanged")
        if skipped:
            parts.append(f"{skipped} skipped")
        summary = ", ".join(parts) if parts else "nothing to do"

        if dry_run:
            self.stdout.write(f"Dry run: {summary}.")
        else:
            self.stdout.write(self.style.SUCCESS(f"{summary.capitalize()}."))
