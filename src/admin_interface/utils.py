"""
admin_interface.utils
~~~~~~~~~~~~~~~~~~~~~
Python-callable utilities for installing bundled themes from pip packages.

Call install_bundled_theme() from AppConfig.ready() via a post_migrate
signal in theme packages (e.g. ophix-theme-imago).
"""

import json
import os
import shutil
import tempfile
from pathlib import Path

from django.apps import apps as django_apps
from django.conf import settings
from django.core import management


def install_bundled_theme(app_config):
    """
    Install themes bundled inside a Django app.

    Looks for one or more theme directories under ``<app>/themes/``, each
    containing a ``theme.json`` fixture and an optional ``media/``
    subdirectory.

    Media files are copied to ``MEDIA_ROOT`` under namespaced paths
    ``admin-interface/themes/<ThemeName>/logo/``,
    ``admin-interface/themes/<ThemeName>/logo_dark/``, and
    ``admin-interface/themes/<ThemeName>/favicon/`` — consistent with the
    upload_to paths set on the Theme model.

    Themes are always installed with ``active=False`` regardless of the
    value in the JSON — activation is left to the operator.

    If a theme with the same name already exists the install is skipped
    (idempotent — safe to call on every migrate run).

    Parameters
    ----------
    app_config
        The AppConfig instance of the app that owns the theme(s).

    Returns
    -------
    list[str]
        Names of themes that were newly installed.
    """
    Theme = django_apps.get_model("admin_interface", "Theme")

    app_path = Path(app_config.path)
    themes_dir = app_path / "themes"

    if not themes_dir.exists():
        return []

    installed = []

    for theme_dir in sorted(themes_dir.iterdir()):
        if not theme_dir.is_dir():
            continue

        json_file = theme_dir / "theme.json"
        if not json_file.exists():
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            continue

        theme_name = data[0]["fields"]["name"]
        already_exists = Theme.objects.filter(name=theme_name).exists()

        if not already_exists:
            # Force inactive on install; strip pk for portability
            for obj in data:
                obj["fields"]["active"] = False
                obj.pop("pk", None)

                # Ensure media paths use the namespaced convention
                for field_name in ("logo", "logo_dark", "favicon"):
                    media_path = obj["fields"].get(field_name)
                    if media_path:
                        filename = Path(media_path).name
                        obj["fields"][field_name] = "admin-interface/themes/{}/{}/{}".format(
                            theme_name, field_name, filename
                        )

            fd, temp_path = tempfile.mkstemp(suffix=".json")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(data, f)
                management.call_command("loaddata", temp_path, verbosity=0)
            finally:
                os.unlink(temp_path)

            installed.append(theme_name)

        # Always copy media files — ensures assets land correctly even if the
        # theme row existed already (e.g. after a package upgrade or path fix).
        media_dir = theme_dir / "media"
        media_root = getattr(settings, "MEDIA_ROOT", None)

        if media_dir.exists():
            if media_root:
                media_root = Path(media_root)
                for src in media_dir.rglob("*"):
                    if src.is_file():
                        # Infer field type from the first subdirectory under media/
                        # Expected layout: media/<field_name>/<filename>
                        parts = src.relative_to(media_dir).parts
                        field_name = parts[0] if len(parts) > 1 else "logo"
                        dst = (
                            media_root
                            / "admin-interface"
                            / "themes"
                            / theme_name
                            / field_name
                            / src.name
                        )
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
            elif not already_exists:
                import warnings
                warnings.warn(
                    "Theme '{}' installed but MEDIA_ROOT is not configured — "
                    "logo and favicon will not be served.".format(theme_name),
                    stacklevel=2,
                )

    return installed
