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
            "export_command": "export_theme",
            "encrypted": False,
            "stable": True,
        },
    ]
