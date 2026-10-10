plugin_category = "core"
plugin_sort = 20

from admin_interface.metadata import (
    __author__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
)

__all__ = [
    "__author__",
    "__copyright__",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
]


def get_revisions_targets():
    """
    Optional hook discovered by ophix-revisions (if installed).
    """
    return [
        {
            "name": "theme",
            "app_label": "admin_interface",
            # Precise model match — Theme rows only.
            "models": ["admin_interface.theme"],
            # export_themes (plural, new) — not export_theme (singular),
            # which exports exactly one named theme + its media as a
            # tar.gz, the wrong shape for revisions. export_themes dumps
            # every theme's field values as plain JSON, no media, matching
            # every other target's export/import convention so cherry-pick
            # restore works the same way here as everywhere else.
            "records_key": "themes",
            "export_command": "export_themes",
            "encrypted": False,
            "stable": True,
        },
    ]
