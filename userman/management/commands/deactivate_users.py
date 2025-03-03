from django.core.management.base import BaseCommand
from django.utils import timezone
from userman.models import Users  # Import your Users model

class Command(BaseCommand):
    help = "Deactivate users whose masaberlaku2 has expired"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        expired_users = Users.objects.filter(masaberlaku2__lte=today, is_active=True)
        count = expired_users.update(is_active=False)
        count = expired_users.update(pending=False)
        self.stdout.write(self.style.SUCCESS(f"Deactivated {count} user(s)"))
