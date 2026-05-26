from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

Theme = apps.get_model("admin_interface", "Theme")


class Command(BaseCommand):
    help = "Set the active Theme by name"

    def add_arguments(self, parser):
        parser.add_argument(
            "theme_name",
            type=str,
            help="Name of the theme to activate",
        )
        parser.add_argument(
            "--no-collectstatic",
            action="store_true",
            help="Skip running collectstatic after activating the theme",
        )

    def handle(self, *args, **options):
        theme_name = options["theme_name"]

        try:
            new_theme = Theme.objects.get(name=theme_name)
        except Theme.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Theme '{theme_name}' not found."))
            return

        if new_theme.active:
            self.stdout.write(f"Theme '{theme_name}' is already active.")
            return

        old_actives = list(Theme.objects.filter(active=True))
        Theme.objects.filter(active=True).update(active=False)

        new_theme.active = True
        new_theme.save()

        if old_actives:
            old_names = ", ".join(t.name for t in old_actives)
            self.stdout.write(self.style.SUCCESS(
                f"Activated theme '{new_theme.name}'. Previously active: {old_names}"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Activated theme '{new_theme.name}'."
            ))

        if not new_theme.title:
            self.stdout.write(self.style.WARNING(
                "This theme has no title set. Run: ophix-manage set_title"
            ))

        if not settings.DEBUG and not options["no_collectstatic"]:
            self.stdout.write("Running collectstatic...")
            call_command("collectstatic", "--noinput", verbosity=1)
            service_name = getattr(settings, "SERVICE_NAME", "").strip()
            restart_cmd = f"sudo systemctl restart {service_name}" if service_name else "sudo systemctl restart <service-name>"
            self.stdout.write(self.style.WARNING(
                f"Restart the service for the updated static files to take effect: {restart_cmd}"
            ))
        elif settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                "DEBUG=True — skipping collectstatic. Reload the page to see the new theme."
            ))
