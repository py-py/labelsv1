import os
import random
from dotenv import load_dotenv
from faker import Faker
from django.core.management import BaseCommand

from label.models import *

load_dotenv()
ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')
ASPECT_RATIO = int(os.getenv('ASPECT_RATIO', '1'))


class Command(BaseCommand):
    def handle(self, *args, **options):
        if ENVIRONMENT == 'prod':
            self.stdout.write(self.style.SUCCESS('Production server does not need to have a FAKE data.'))
            return

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
            image.save(image_url=image_template.format(height=ASPECT_RATIO * 500, width=1 * 500))
        self.stdout.write(self.style.SUCCESS('{count} labels were created.'.format(count=count_label)))
