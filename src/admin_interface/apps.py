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

        from django.db.models.signals import post_migrate
        post_migrate.connect(_install_ophix_theme, sender=self)


def _install_ophix_theme(sender, **kwargs):
    from admin_interface.utils import install_bundled_theme

    install_bundled_theme(sender)
