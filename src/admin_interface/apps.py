from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminInterfaceConfig(AppConfig):
    name = "admin_interface"
    verbose_name = _("Appearance")
    admin_order = 800
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from admin_interface import settings

        settings.check_installed_apps()

        from django.db.models.signals import post_migrate, post_save
        post_migrate.connect(_install_ophix_theme, sender=self)

        from admin_interface.models import Theme
        post_save.connect(_on_theme_save, sender=Theme)


def _install_ophix_theme(sender, **kwargs):
    from admin_interface.utils import install_bundled_theme

    install_bundled_theme(sender)


def _on_theme_save(sender, instance, **kwargs):
    """Regenerate static error pages when an active theme is saved."""
    if not instance.active:
        return
    try:
        from pathlib import Path
        from django.conf import settings as django_settings
        install_dir = getattr(django_settings, "INSTALL_DIR", None)
        if install_dir is None:
            return
        error_pages_dir = Path(install_dir) / "static" / "error_pages"
        if not error_pages_dir.is_dir():
            return
        from django.core.management import call_command
        call_command("generate_error_pages", verbosity=0)
    except Exception:
        pass
