import gzip
import json
import re
import shutil
import tarfile
import tempfile
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


def _zero_tarinfo(tarinfo):
    """tarfile.add()'s `filter` callback for --stable: every entry's mtime
    and ownership metadata otherwise reflects real filesystem state (when
    the file was written into the temp export dir, and by which uid/gid),
    which differs run-to-run even for byte-identical content."""
    tarinfo.mtime = 0
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.uname = ""
    tarinfo.gname = ""
    return tarinfo


class Command(BaseCommand):
    help = "Export a Theme (with media) to a self-contained tar.gz"

    def add_arguments(self, parser):
        parser.add_argument(
            "theme_name",
            type=str,
            help="The name of the theme to export",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Output directory for the exported theme tar.gz",
        )
        parser.add_argument(
            "--rename",
            type=str,
            default=None,
            help="Rename the theme inside the exported JSON (also affects paths and tar.gz name)",
        )
        parser.add_argument(
            "--stable",
            action="store_true",
            help="Produce a byte-identical archive across runs of the same unchanged "
                 "theme (deterministic JSON key order, zeroed tar entry mtimes/ownership, "
                 "zeroed gzip header timestamp). Used by ophix-revisions.",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")
        theme_name = options["theme_name"]
        output_dir = Path(options["output"] or settings.BASE_DIR)
        rename = options["rename"]
        stable = options["stable"]

        try:
            theme = Theme.objects.get(name=theme_name)
        except Theme.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Theme '{theme_name}' not found"))
            return

        export_name = rename or theme_name
        self.stdout.write(f"Exporting theme '{theme_name}'...")

        export_dir = Path(tempfile.mkdtemp())
        try:
            theme_dir = export_dir / export_name
            theme_dir.mkdir()

            json_path = theme_dir / "theme.json"
            with open(json_path, "w", encoding="utf-8") as f:
                management.call_command(
                    "dumpdata",
                    "admin_interface.theme",
                    "--indent", "2",
                    "--pks", str(theme.pk),
                    stdout=f,
                )

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for obj in data:
                fields = obj.get("fields", {})
                obj.pop("pk", None)

                if rename:
                    fields["name"] = rename

                for field_name in ("logo", "favicon"):
                    media_path = fields.get(field_name)
                    if media_path:
                        media_path = str(media_path)
                        match = re.match(
                            r"^admin-interface/themes/([^/]+)/(logo|favicon)/(.+)$",
                            media_path,
                        )
                        filename = Path(media_path).name
                        if match:
                            fields[field_name] = (
                                f"admin-interface/themes/{export_name}/{match[2]}/{match[3]}"
                            )
                        else:
                            fields[field_name] = (
                                f"admin-interface/themes/{export_name}/{field_name}/{filename}"
                            )

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, sort_keys=stable)

            for field_name in ("logo", "favicon"):
                field_file = getattr(theme, field_name)
                if field_file and field_file.name:
                    src_path = Path(field_file.path)
                    if not src_path.exists():
                        self.stdout.write(self.style.WARNING(
                            f"Media file not found: {src_path}"
                        ))
                        continue

                    dest_relative_path = None
                    for obj in data:
                        dest_relative_path = obj["fields"].get(field_name)
                        if dest_relative_path:
                            break
                    if not dest_relative_path:
                        dest_relative_path = field_file.name

                    dst_path = theme_dir / "media" / dest_relative_path
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    self.stdout.write(f"Copied media file: {dest_relative_path}")

            tar_path = output_dir / f"{export_name}_theme.tar.gz"
            if stable:
                # tarfile.open(path, "w:gz")'s built-in gzip shortcut writes
                # the current wall-clock time into the gzip header's own
                # MTIME field, with no way to override it via that API —
                # constructing the GzipFile explicitly (mtime=0, no embedded
                # filename) and handing it to tarfile as a fileobj is the
                # only way to zero that second, independent timestamp source.
                with open(tar_path, "wb") as raw_f:
                    with gzip.GzipFile(filename="", fileobj=raw_f, mode="wb", mtime=0) as gz_f:
                        with tarfile.open(fileobj=gz_f, mode="w:") as tar:
                            tar.add(theme_dir, arcname=export_name, filter=_zero_tarinfo)
            else:
                with tarfile.open(tar_path, "w:gz") as tar:
                    tar.add(theme_dir, arcname=export_name)

        finally:
            shutil.rmtree(export_dir, ignore_errors=True)

        self.stdout.write(self.style.SUCCESS(f"Theme exported to {tar_path}"))
