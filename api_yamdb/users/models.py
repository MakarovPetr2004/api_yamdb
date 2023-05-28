from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True, blank=False, validators=[validate_email])
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        max_length=1024,
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=5,
        verbose_name='Код подтверждения',
        blank=True
    )
