import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import (
    User, Title, Genre, Category, Genre_title, Review, Comment
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        CSV_DIR = Path('static', 'data')
        TITLES = (
            ('category.csv', Category, {}),
            ('genre.csv', Genre, {}),
            ('users.csv', User, {}),
            ('titles.csv', Title, {'category': 'category_id'}),
            ('genre_title.csv', Genre_title, {}),
            ('review.csv', Review, {'author': 'author_id'}),
            ('comments.csv', Comment, {'author': 'author_id'}),
        )
        for file, model, replace in TITLES:
            with open(Path(CSV_DIR, file), mode='r', encoding='utf8') as f:
                reader = csv.DictReader(f)
                counter = 0
                objects_to_create = []
                for row in reader:
                    counter += 1
                    args = dict(**row)
                    if replace:
                        for old, new in replace.items():
                            args[new] = args.pop(old)
                    objects_to_create.append(model(**args))
                model.objects.bulk_create(objects_to_create,
                                          ignore_conflicts=True)
        self.stdout.write("Все данные загружены!")
