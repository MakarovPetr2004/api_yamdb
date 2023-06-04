from django.db import models

from users.models import User

from .validators import validate_max_min, validate_year


class CategoryGenreClass(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(CategoryGenreClass):

    class Meta(CategoryGenreClass.Meta):
        verbose_name = 'Категория'


class Genre(CategoryGenreClass):

    class Meta(CategoryGenreClass.Meta):
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField('Название произведения',
                            max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField('Описание')
    rating = models.PositiveSmallIntegerField(
        'Рейтинг произведения',
        blank=True,
        null=True,
        validators=[validate_max_min]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genre_title',
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
    )


class Genre_title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genres',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_combination_gt'
            )
        ]


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[validate_max_min],
        default=0,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
