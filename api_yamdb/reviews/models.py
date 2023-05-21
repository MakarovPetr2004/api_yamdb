from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_max_min
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveIntegerField('Год выпуска')
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
    )
    
    
class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[validate_max_min],
        default=5
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
