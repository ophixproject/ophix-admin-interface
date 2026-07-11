import importlib.util
import json
from importlib.metadata import entry_points
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand


def _build_theme_package_map():
    """Map each theme's declared name (theme.json fields.name) to its
    source package. Keyed by declared name, not the on-disk folder name —
    a theme's folder name is an implementation detail and isn't guaranteed
    to match its display name (e.g. a folder "IceQueen" whose theme.json
    declares "Ice Queen")."""
    mapping = {}
    try:
        eps = entry_points(group="ophix.plugins")
    except Exception:
        return mapping

    for ep in eps:
        try:
            dist = ep.dist
            pkg_name = dist.name
            pkg_version = dist.version
        except Exception:
            pkg_name = ep.name
            pkg_version = "?"

        try:
            spec = importlib.util.find_spec(ep.value)
            if not spec or not spec.origin:
                continue
            theme_dir = Path(spec.origin).parent / "themes"
            if not theme_dir.is_dir():
                continue
            for d in sorted(theme_dir.iterdir()):
                json_file = d / "theme.json"
                if not d.is_dir() or not json_file.exists():
                    continue
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    theme_name = data[0]["fields"]["name"]
                except Exception:
                    theme_name = d.name
                mapping[theme_name] = (pkg_name, pkg_version)
        except Exception:
            continue

    return mapping


class Command(BaseCommand):
    help = "List all available Themes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--details",
            action="store_true",
            help="Show detailed info for each theme including source package and version",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")
        themes = Theme.objects.all()
        if not themes.exists():
            self.stdout.write("No themes found.")
            return

        if not options["details"]:
            for theme in themes:
                self.stdout.write(theme.name)
            return

        pkg_map = _build_theme_package_map()

        headers = ["ID", "Name", "Active", "Package", "Version"]
        rows = []

        for theme in themes:
            pkg_name, pkg_version = pkg_map.get(theme.name, ("-", "-"))
            rows.append([
                str(theme.id),
                theme.name,
                "Yes" if theme.active else "No",
                pkg_name,
                pkg_version,
            ])

        col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]
        fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)

        self.stdout.write(fmt.format(*headers))
        self.stdout.write("-+-".join("-" * w for w in col_widths))

        for row in rows:
            self.stdout.write(fmt.format(*row))
