from django.db import models

from . import const
from users.models import User
from .validators import validate_max_min


class Category(models.Model):
    name = models.CharField(max_length=const.MAX_LEN_NAMES)
    slug = models.SlugField(unique=True, max_length=const.MAX_LEN_SLUG)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=const.MAX_LEN_NAMES)
    slug = models.SlugField(unique=True, max_length=const.MAX_LEN_SLUG)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=const.MAX_LEN_NAMES
    )
    year = models.PositiveIntegerField('Год выпуска')
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
    )

    class Meta:
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


class AbstractCommentReview(models.Model):
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
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author} в {self.pub_date} написал: {self.text}'


class Review(AbstractCommentReview):
    score = models.SmallIntegerField(
        'Оценка',
        validators=[validate_max_min],
        default=1,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta(AbstractCommentReview.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(AbstractCommentReview):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta(AbstractCommentReview.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
