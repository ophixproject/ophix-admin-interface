from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminInterfaceConfig(AppConfig):
    name = "admin_interface"
    verbose_name = _("Admin Interface")
    admin_order = 800
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from admin_interface import settings

        settings.check_installed_apps()

        from django.db.models.signals import post_migrate
        post_migrate.connect(_install_ophix_theme, sender=self)


def _install_ophix_theme(sender, **kwargs):
    from django.apps import apps
    from django.conf import settings
    from admin_interface.utils import install_bundled_theme

    install_bundled_theme(sender)

    # Populate the Ophix theme title from SERVER_NAME if it is still empty.
    # Only fills in a blank — never overwrites a title the operator has set.
    Theme = apps.get_model("admin_interface", "Theme")
    try:
        ophix_theme = Theme.objects.get(name="Ophix")
        if not ophix_theme.title:
            server_name = getattr(settings, "SERVER_NAME", "").strip()
            ophix_theme.title = ("Ophix " + server_name).strip() if server_name else "Ophix"
            ophix_theme.save(update_fields=["title"])
    except Theme.DoesNotExist:
        pass
