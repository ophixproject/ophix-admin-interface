"""
ophix-manage generate_error_pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate static HTML error pages styled with the current active theme.

Output files are written to INSTALL_DIR/static/error_pages/ by default.
Nginx error_page directives in the generated nginx.conf point to these files.

Called automatically:
  - At the end of ophix-manage run_install
  - When the active theme is saved (post_save signal in apps.py)

Usage::

    ophix-manage generate_error_pages
    ophix-manage generate_error_pages --codes 404,500,503
    ophix-manage generate_error_pages --output-dir /path/to/error_pages/
"""

from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string


_ERROR_DEFINITIONS = {
    400: ("Bad Request", "The server could not process your request."),
    403: ("Forbidden", "You do not have permission to access this page."),
    404: ("Page Not Found", "The page you are looking for could not be found."),
    500: ("Server Error", "An unexpected error occurred. Please try again later."),
    503: ("Service Unavailable", "The server is temporarily unavailable. Please try again shortly."),
}

_DEFAULT_CODES = [400, 403, 404, 500, 503]


class Command(BaseCommand):
    help = "Generate static HTML error pages styled with the active theme."

    def add_arguments(self, parser):
        parser.add_argument(
            "--codes",
            metavar="CODES",
            help=(
                "Comma-separated list of HTTP status codes to generate. "
                f"Default: {','.join(str(c) for c in _DEFAULT_CODES)}"
            ),
        )
        parser.add_argument(
            "--output-dir",
            metavar="DIR",
            help=(
                "Directory to write HTML files into. "
                "Default: INSTALL_DIR/static/error_pages/"
            ),
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress per-file output.",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")
        try:
            theme = Theme.objects.get(active=True)
        except Theme.DoesNotExist:
            raise CommandError("No active theme found. Activate a theme first.")

        # ServerSettings is optional (ophix-admin-settings may not be installed)
        server_settings = None
        try:
            ServerSettings = apps.get_model("ophix_admin_settings", "ServerSettings")
            server_settings = ServerSettings.objects.first()
        except LookupError:
            pass

        server_name = getattr(settings, "SERVER_NAME", "Ophix")

        site_title = (
            (server_settings.title if server_settings and server_settings.title else None)
            or server_name
            or "Ophix"
        )

        logo_url = ""
        if theme.logo:
            try:
                logo_url = theme.logo.url
            except Exception:
                pass

        logo_visible = getattr(theme, "logo_visible", True)
        logo_max_width = getattr(theme, "logo_max_width", 400) or 400
        logo_max_height = getattr(theme, "logo_max_height", 100) or 100
        logo_vertical_offset = getattr(theme, "logo_vertical_offset", 0) or 0
        title_font_size = getattr(theme, "title_font_size", "") or ""

        # Determine output directory
        if options.get("output_dir"):
            output_dir = Path(options["output_dir"])
        else:
            install_dir = getattr(settings, "INSTALL_DIR", None)
            if install_dir:
                output_dir = Path(install_dir) / "static" / "error_pages"
            else:
                output_dir = Path.cwd() / "static" / "error_pages"

        output_dir.mkdir(parents=True, exist_ok=True)

        # Determine which codes to generate
        if options.get("codes"):
            try:
                codes = [int(c.strip()) for c in options["codes"].split(",") if c.strip()]
            except ValueError:
                raise CommandError("--codes must be a comma-separated list of integers.")
        else:
            codes = list(_DEFAULT_CODES)

        quiet = options.get("quiet", False)
        if not quiet:
            self.stdout.write(f"Writing error pages to {output_dir}\n")

        for code in codes:
            title, message = _ERROR_DEFINITIONS.get(code, ("Error", "An error occurred."))
            ctx = {
                "theme": theme,
                "server_settings": server_settings,
                "server_name": server_name,
                "site_title": site_title,
                "logo_url": logo_url,
                "logo_visible": logo_visible,
                "logo_max_width": logo_max_width,
                "logo_max_height": logo_max_height,
                "logo_vertical_offset": logo_vertical_offset,
                "title_font_size": title_font_size,
                "error_code": code,
                "error_title": title,
                "error_message": message,
            }
            html = render_to_string(
                "admin_interface/error_pages/error_page.html", ctx
            )
            out_path = output_dir / f"{code}.html"
            out_path.write_text(html, encoding="utf-8")
            if not quiet:
                self.stdout.write(self.style.SUCCESS(f"  {out_path.name}"))

        if not quiet:
            self.stdout.write("")
