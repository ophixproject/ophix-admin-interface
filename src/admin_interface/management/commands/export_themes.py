"""
ophix-manage export_themes
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Export every Theme's field values (metadata only, no logo/favicon image
bytes) to a JSON file — for backup, server migration, or ophix-revisions'
git-backed history.

This is deliberately separate from `export_theme` (singular), which exports
exactly one named theme as a self-contained tar.gz bundle including its
logo/favicon media — the right tool for transferring a specific theme
between servers. `export_themes` (plural) exports every theme that exists,
not just the active one, as plain JSON with no bundled media: binary image
diffs aren't meaningful in a git history, and a theme can be edited while
inactive, so tracking changes only to whichever theme happens to be active
would silently miss history for every other one.

`logo`/`favicon` are included as plain path strings (the same way every
other field is) — restoring from this file never recreates the actual
image file, only the field value pointing at where it used to be.

Use --stable to omit the meta block and sort keys, so re-exporting
unchanged themes produces byte-identical output (used by ophix-revisions).

Examples
--------
Export every theme:
    ophix-manage export_themes --output-file themes.json

Deterministic export (for ophix-revisions):
    ophix-manage export_themes --output-file themes.json --stable

Preview without writing:
    ophix-manage export_themes --output-file themes.json --dry-run
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


def _build_meta(command: str) -> dict:
    import datetime
    import os
    import socket

    try:
        import pwd
        run_by = pwd.getpwuid(os.getuid()).pw_name
    except Exception:
        run_by = os.environ.get("USER") or os.environ.get("LOGNAME")

    from django.conf import settings
    ssh_raw = os.environ.get("SSH_CLIENT", "")
    return {
        "created_at":     datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "server_name":    getattr(settings, "SERVER_NAME", None),
        "server_version": getattr(settings, "SERVER_VERSION", None),
        "hostname":       socket.gethostname(),
        "command":        command,
        "run_by":         run_by,
        "login_user":     os.environ.get("SUDO_USER") or None,
        "ssh_origin":     ssh_raw.split()[0] if ssh_raw else None,
    }


def _dump_themes() -> list:
    """Every Theme row's field values, flattened from Django's own fixture
    format (pk kept separate from fields there) into one flat dict per
    theme. dumpdata is used specifically because Theme has ~150 fields —
    hand-listing them the way every other export command's _serialize()
    does would be impractical and a maintenance trap every time a field is
    added. No FK/M2M fields exist on Theme, so this flattening is safe."""
    import io

    from django.apps import apps
    from django.core import management

    Theme = apps.get_model("admin_interface", "Theme")

    buf = io.StringIO()
    management.call_command(
        "dumpdata", "admin_interface.theme", "--indent", "2", stdout=buf
    )
    raw = json.loads(buf.getvalue() or "[]")

    themes = [dict(obj["fields"]) for obj in raw]
    themes.sort(key=lambda t: (t.get("name") or "").lower())
    return themes


class Command(BaseCommand):
    help = "Export every Theme's field values (no media) to a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-file",
            required=True,
            metavar="FILE",
            help="Destination file path.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many themes would be exported without writing anything.",
        )
        parser.add_argument(
            "--stable",
            action="store_true",
            help="Omit the meta block and sort keys, so re-exporting unchanged themes "
                 "produces byte-identical output (used by ophix-revisions).",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress all output.",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output_file"])
        dry_run     = options["dry_run"]
        stable      = options["stable"]
        quiet       = options["quiet"]

        themes = _dump_themes()
        count = len(themes)

        if dry_run:
            self.stdout.write(f"Dry run: {count} theme(s) would be exported to {output_path}.")
            return

        if count == 0:
            if not quiet:
                self.stdout.write("No themes found — nothing to export.")
            return

        if not output_path.parent.exists():
            raise CommandError(f"Output directory does not exist: {output_path.parent}")

        payload = {"version": 1}
        if not stable:
            payload["meta"] = _build_meta("export_themes")
        payload["themes"] = themes

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=stable)

        if not quiet:
            self.stdout.write(self.style.SUCCESS(f"Exported {count} theme(s) to {output_path}."))
