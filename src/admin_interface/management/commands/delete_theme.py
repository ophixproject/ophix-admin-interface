from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete a Theme by name, including its namespaced media directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "theme_name",
            type=str,
            help="Name of the theme to delete",
        )
        parser.add_argument(
            "--preserve-media",
            action="store_true",
            help="Do NOT delete referenced media files or namespaced directory",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force deletion even if theme is active (NOT recommended)",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")
        theme_name = options["theme_name"]
        preserve_media = options["preserve_media"]
        force = options["force"]

        try:
            theme = Theme.objects.get(name=theme_name)
        except Theme.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Theme '{theme_name}' not found."))
            return

        if theme.active and not force:
            self.stderr.write(self.style.ERROR(
                f"Cannot delete active theme '{theme_name}'. "
                "Use set_theme first, or pass --force."
            ))
            return

        if Theme.objects.count() == 1:
            self.stderr.write(self.style.ERROR(
                "Refusing to delete the last remaining theme. "
                "The system must have at least one theme."
            ))
            return

        theme_media_dir = Path(settings.MEDIA_ROOT) / "admin-interface" / "themes" / theme_name
        has_media = theme_media_dir.exists()

        theme._preserve_media = preserve_media
        theme.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted theme '{theme_name}'."))
        if preserve_media:
            self.stdout.write("Preserved media files/directories.")
        elif has_media:
            self.stdout.write(f"Deleted media: {theme_media_dir}")
        else:
            self.stdout.write("No media directory found.")
