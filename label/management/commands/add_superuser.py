import os
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_dotenv()
        username = os.getenv('SUPERUSER_USERNAME')
        password = os.getenv('SUPERUSER_PASSWORD')
        email = os.getenv('SUPERUSER_EMAIL')
        try:
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
        except IntegrityError as exc:
            pass
        finally:
            self.stdout.write(self.style.SUCCESS('Superuser was created.'))
