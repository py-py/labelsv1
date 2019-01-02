import os
import random

from django.core.management import BaseCommand
from faker import Faker

from label.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        image_template = 'https://placeimg.com/{width}/{height}/any'
        count_manufactures = int(os.getenv('FAKE_MANUFACTURES', 3))
        count_kinds = int(os.getenv('FAKE_KINDS', 3))
        count_label = int(os.getenv('FAKE_LABELS', 10))

        # MANUFACTURE
        manufactures = []
        for _ in range(count_manufactures):
            manufacture = Manufacture.objects.create(name=fake.name())
            manufactures.append(manufacture)
        self.stdout.write(self.style.SUCCESS('{count} manufactures were created.'.format(count=count_manufactures)))

        # KIND
        kinds = []
        for _ in range(count_kinds):
            kind = Kind.objects.create(name=fake.name())
            kinds.append(kind)
        self.stdout.write(self.style.SUCCESS('{count} kinds were created.'.format(count=count_kinds)))

        for _ in range(count_label):
            label = Label(
                manufacture=random.choice(manufactures),
                kind=random.choice(kinds),
                name=fake.name(),
                year=fake.year()
            )
            label.save()
            image = Image(label=label)
            image.save(image_url=image_template.format(width=400, height=500))
        self.stdout.write(self.style.SUCCESS('{count} labels were created.'.format(count=count_label)))
