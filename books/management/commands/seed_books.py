from random import choice, randint
from django.core.management.base import BaseCommand
from django_seed import Seed
from books.models import Book
from categories.models import Category
from people.models import Person


class Command(BaseCommand):

    help = "This command seeds books"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--total", help="How many books do you want to create?", default=10
    #     )

    def handle(self, *args, **options):
        # total = int(options.get("total"))
        total = 40
        categories = Category.objects.all()
        writers = Person.objects.filter(kind=Person.KIND_WRITER)
        seeder = Seed.seeder()
        seeder.add_entity(
            Book,
            total,
            {
                "year": lambda x: seeder.faker.year(),
                "category": lambda x: choice(categories),
                "writer": lambda x: choice(writers),
                "cover_image": lambda x: f"book_cover_images/{randint(1, 15)}.jpg",
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} books created!"))
