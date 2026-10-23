from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from portal.models import Application, SecurityGroup

GROUPS = ["admin", "manager", "developer", "test"]

# email -> groups (change these assignments to what you want)
USERS = {
    "user1@example.com": ["admin"],
    "user2@example.com": ["developer"],
}


class Command(BaseCommand):
    help = "Create initial groups, users and the django-portal application."

    def handle(self, *args, **options):
        groups = {}
        for name in GROUPS:
            groups[name], _ = SecurityGroup.objects.get_or_create(name=name)

        for email, group_names in USERS.items():
            user, created = User.objects.get_or_create(
                username=email,
                defaults={"email": email},
            )
            if created:
                user.set_password("pass")#user.set_unusable_password()  # login is via authentik only
                user.save()
            for g in group_names:
                groups[g].users.add(user)

        app, _ = Application.objects.get_or_create(
            id="django-portal",
            defaults={
                "name": "Django Portal",
                "service": "django-portal",
                "enabled": True,
            },
        )
        app.groups.set(groups.values())

        self.stdout.write(self.style.SUCCESS("Seed complete."))