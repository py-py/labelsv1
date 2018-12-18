import os
import random

from django.core.management import BaseCommand
from faker import Faker

from label.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        image_template = 'https://placeimg.com/{width}/{height}/any'
        count_manufactories = int(os.getenv('FAKE_MANUFACTORIES', 10))
        count_kinds = int(os.getenv('FAKE_KINDS', 10))
        count_label = int(os.getenv('FAKE_LABELS', 100))

        # MANUFACTORY
        manufactories = []
        for _ in range(count_manufactories):
            manufactory = Manufactory.objects.create(name=fake.name())
            manufactories.append(manufactory)
        self.stdout.write(self.style.SUCCESS(f'{count_manufactories} manufactories were created.'))

        # KIND
        kinds = []
        for _ in range(count_kinds):
            kind = Kind.objects.create(name=fake.name())
            kinds.append(kind)
        self.stdout.write(self.style.SUCCESS(f'{count_kinds} kinds were created.'))

        for _ in range(count_label):
            label = Label(
                manufactory=random.choice(manufactories),
                kind=random.choice(kinds),
                name=fake.name(),
                year=fake.year()
            )
            label.save()
            image = Image(label=label)
            image.save(image_url=image_template.format(width=400, height=500))