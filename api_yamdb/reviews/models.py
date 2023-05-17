from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_max_min

User = get_user_model()


class Title(models.Model):
    # Сюда Полина добавит код для произведений
    pass


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[validate_max_min]
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
