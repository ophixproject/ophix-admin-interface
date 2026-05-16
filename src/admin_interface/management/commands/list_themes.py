import importlib.util
from importlib.metadata import entry_points
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand


def _build_theme_package_map():
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
                if d.is_dir() and (d / "theme.json").exists():
                    mapping[d.name] = (pkg_name, pkg_version)
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

        headers = ["ID", "Name", "Active", "Title", "Env Name", "Package", "Version"]
        rows = []

        for theme in themes:
            pkg_name, pkg_version = pkg_map.get(theme.name, ("-", "-"))
            rows.append([
                str(theme.id),
                theme.name,
                "Yes" if theme.active else "No",
                theme.title or "-",
                theme.env_name or "-",
                pkg_name,
                pkg_version,
            ])

        col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]
        fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)

        self.stdout.write(fmt.format(*headers))
        self.stdout.write("-+-".join("-" * w for w in col_widths))

        for row in rows:
            self.stdout.write(fmt.format(*row))
