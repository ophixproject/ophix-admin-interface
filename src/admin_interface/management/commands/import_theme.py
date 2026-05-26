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


class Command(BaseCommand):
    help = "Import a Theme from a tar.gz exported with export_theme"

    def add_arguments(self, parser):
        parser.add_argument(
            "tar_file",
            type=str,
            help="Path to the theme tar.gz file to import",
        )
        parser.add_argument(
            "--rename",
            type=str,
            default=None,
            help="Rename the theme during import",
        )
        parser.add_argument(
            "--title",
            type=str,
            default=None,
            help="Override title during import",
        )
        parser.add_argument(
            "--env-name",
            type=str,
            default=None,
            help="Override env_name during import",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing theme if one with the same name exists",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")
        tar_path = Path(options["tar_file"]).resolve()
        rename = options["rename"]
        title_override = options["title"]
        env_override = options["env_name"]
        force = options["force"]

        if not tar_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {tar_path}"))
            return

        self.stdout.write(f"Importing theme from {tar_path}...")

        temp_dir = Path(tempfile.mkdtemp())
        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=temp_dir)

            extracted_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
            if not extracted_dirs:
                self.stderr.write(self.style.ERROR("No folder found inside archive"))
                return

            extracted_theme_dir = extracted_dirs[0]
            json_file = extracted_theme_dir / "theme.json"
            if not json_file.exists():
                self.stderr.write(self.style.ERROR("theme.json not found in archive"))
                return

            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not data:
                self.stderr.write(self.style.ERROR("No theme data found in JSON"))
                return

            original_name = data[0]["fields"]["name"]
            theme_name = rename or original_name

            existing = Theme.objects.filter(name=theme_name)
            if existing.exists() and not force:
                self.stderr.write(self.style.ERROR(
                    f"A theme named '{theme_name}' already exists. Use --force to overwrite."
                ))
                return

            if existing.exists() and force:
                existing.delete()
                self.stdout.write(f"Deleted existing theme '{theme_name}' due to --force flag.")

            for obj in data:
                fields = obj.get("fields", {})
                obj.pop("id", None)
                fields["name"] = theme_name

                if title_override is not None:
                    fields["title"] = title_override
                if env_override is not None:
                    fields["env_name"] = env_override

                for field_name in ("logo", "favicon"):
                    media_path = fields.get(field_name)
                    if media_path:
                        media_path = str(media_path)
                        match = re.match(
                            r"^admin-interface/themes/([^/]+)/(logo|favicon)/(.+)$",
                            media_path,
                        )
                        if match:
                            fields[field_name] = (
                                f"admin-interface/themes/{theme_name}/{match[2]}/{match[3]}"
                            )
                        else:
                            filename = Path(media_path).name
                            fields[field_name] = (
                                f"admin-interface/themes/{theme_name}/{field_name}/{filename}"
                            )

            temp_json_path = extracted_theme_dir / "theme_mutated.json"
            with open(temp_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            management.call_command("loaddata", str(temp_json_path), verbosity=0)
            self.stdout.write("Theme data loaded.")

            media_dir = extracted_theme_dir / "media"
            if media_dir.exists():
                for file_path in media_dir.rglob("*"):
                    if file_path.is_file():
                        # Derive destination by substituting the theme name into
                        # the path rather than matching by filename — handles any
                        # field (logo, favicon) without enumeration.
                        parts = list(file_path.relative_to(media_dir).parts)
                        # parts: ['admin-interface', 'themes', '<original>', '<field>', '<file>']
                        if len(parts) >= 3 and parts[1] == "themes":
                            parts[2] = theme_name
                        rel_path = Path(*parts)
                        dst_path = Path(settings.MEDIA_ROOT) / rel_path
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, dst_path)
                        self.stdout.write(f"Copied media file: {rel_path}")
            else:
                self.stdout.write("No media files to copy.")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.stdout.write(self.style.SUCCESS(f"Theme '{theme_name}' imported successfully."))
