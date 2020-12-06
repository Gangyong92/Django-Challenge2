from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="hydjango")
        if not admin:
            User.objects.create_superuser(
                "hydjango", "hyeonggang@naver.com", "hydjango1q2w3e4r"
            )
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
