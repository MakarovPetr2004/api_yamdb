import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Genre_title, Review, Title
from users.models import User


def category(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def titles(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def users(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def review(row):
    title, _ = Title.objects.get_or_create(id=row[1])
    Review.objects.get_or_create(
        id=row[0],
        title=title,
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comment(row):
    review, _ = Review.objects.get_or_create(id=row[1])
    Comment.objects.get_or_create(
        id=row[0],
        review=review,
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


def genre_title(row):
    title, _ = Title.objects.get_or_create(id=row[1])
    genre, _ = Genre.objects.get_or_create(id=row[2])
    Genre_title.objects.get_or_create(
        id=row[0],
        title=title,
        genre=genre,
    )


action = {
    'category.csv': category,
    'genre.csv': genre,
    'titles.csv': titles,
    'users.csv': users,
    'review.csv': review,
    'comments.csv': comment,
    'genre_title.csv': genre_title
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for filename, row in action.items():
            path = os.path.join(settings.BASE_DIR, "static/data/") + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
        self.stdout.write("Все данные загружены!")
