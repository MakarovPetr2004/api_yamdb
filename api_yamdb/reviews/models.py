from django.db import models

from constants import CATEGORY_GENRE_NAME_LEN, CATEGORY_GENRE_SLUG_LEN
from users.models import User
from .validators import validate_max_min, validate_year


class NameSlug(models.Model):
    name = models.CharField(max_length=CATEGORY_GENRE_NAME_LEN)
    slug = models.SlugField(unique=True, max_length=CATEGORY_GENRE_SLUG_LEN)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=CATEGORY_GENRE_NAME_LEN
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genre_title',
        verbose_name='Жанр',
        blank=True,
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genres',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_combination_gt'
            )
        ]


class AuthorTextPubDate(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        'Текст'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author} в {self.pub_date} написал: {self.text}'


class Review(AuthorTextPubDate):
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[validate_max_min],
        default=1,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta(AuthorTextPubDate.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(AuthorTextPubDate):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta(AuthorTextPubDate.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
