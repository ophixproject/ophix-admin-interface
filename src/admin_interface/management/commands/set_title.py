from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set the title on the active theme"

    def add_arguments(self, parser):
        parser.add_argument(
            "title",
            nargs="?",
            type=str,
            help="New title to set (omit to be prompted)",
        )
        parser.add_argument(
            "--use-existing",
            action="store_true",
            help=(
                "Copy the title from a previously active (now inactive) theme "
                "rather than prompting for a new one"
            ),
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the title on the active theme without prompting",
        )

    def handle(self, *args, **options):
        Theme = apps.get_model("admin_interface", "Theme")

        active = Theme.objects.filter(active=True).first()
        if not active:
            self.stderr.write(self.style.ERROR("No active theme found."))
            return

        if options["clear"]:
            new_title = ""
        elif options["title"]:
            new_title = options["title"]
        elif options["use_existing"]:
            candidates = list(
                Theme.objects.filter(active=False)
                .exclude(title="")
                .values_list("title", flat=True)
                .distinct()
            )
            if not candidates:
                self.stderr.write(self.style.ERROR(
                    "No inactive themes with a title found."
                ))
                return
            if len(candidates) == 1:
                new_title = candidates[0]
            else:
                self.stdout.write("Multiple titles found on inactive themes:")
                for i, title in enumerate(candidates, 1):
                    self.stdout.write(f"  {i}. {title}")
                try:
                    choice = input("Enter number: ").strip()
                except KeyboardInterrupt:
                    self.stdout.write("")
                    self.stdout.write("Cancelled. No changes made.")
                    return
                try:
                    new_title = candidates[int(choice) - 1]
                except (ValueError, IndexError):
                    self.stderr.write(self.style.ERROR("Invalid choice."))
                    return
        else:
            current = active.title or ""
            prompt = f"Enter new title [{current}]: " if current else "Enter new title: "
            try:
                entered = input(prompt).strip()
            except KeyboardInterrupt:
                self.stdout.write("")
                self.stdout.write("Cancelled. No changes made.")
                return
            new_title = entered if entered else current

        active.title = new_title
        active.save()

        if new_title:
            self.stdout.write(self.style.SUCCESS(
                f"Title set to '{new_title}' on theme '{active.name}'."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Title cleared on theme '{active.name}'."
            ))
