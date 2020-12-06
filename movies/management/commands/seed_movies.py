from random import choice, randint
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from movies.models import Movie
from categories.models import Category
from people.models import Person


class Command(BaseCommand):

    help = "This command seeds movies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total", help="How many movies do you want to create?", default=10
        )

    def handle(self, *args, **options):
        total = int(options.get("total"))
        categories = Category.objects.all()
        directors = Person.objects.filter(kind=Person.KIND_DIRECTOR)
        seeder = Seed.seeder()
        seeder.add_entity(
            Movie,
            total,
            {
                "year": lambda x: seeder.faker.year(),
                "category": lambda x: choice(categories),
                "director": lambda x: choice(directors),
                "cover_image": lambda x: f"movie_cover_images/{randint(1, 15)}.jpg",
            },
        )
        created_cast = seeder.execute()
        created_clean = flatten(list(created_cast.values()))
        actors = Person.objects.filter(kind=Person.KIND_ACTOR)
        for pk in created_clean:
            movie = Movie.objects.get(pk=pk)
            for a in actors:
                magic_number = randint(0, 15)
                if magic_number % 2 == 0:
                    movie.cast.add(a)
        self.stdout.write(self.style.SUCCESS(f"{total} movies created!"))
