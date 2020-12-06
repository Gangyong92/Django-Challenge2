from random import choice, randint
from django.core.management.base import BaseCommand
from django_seed import Seed
from people.models import Person


class Command(BaseCommand):

    help = "This command seeds people"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--total", help="How many people do you want to create?", default=10
    #     )

    def handle(self, *args, **options):
        # total = int(options.get("total"))
        total = 40
        test_url = (
            "https://django-challenge2-hgy.s3.ap-northeast-2.amazonaws.com/uploads/"
        )
        seeder = Seed.seeder()
        seeder.add_entity(
            Person,
            total,
            {
                "name": lambda x: seeder.faker.name(),
                "kind": lambda x: choice(
                    [Person.KIND_ACTOR, Person.KIND_DIRECTOR, Person.KIND_WRITER]
                ),
                "photo": lambda x: f"{test_url}person_images/{randint(1, 15)}.jpg",
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} people created!"))
