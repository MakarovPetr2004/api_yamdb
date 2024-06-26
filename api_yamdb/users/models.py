from django.contrib.auth.models import AbstractUser
from django.db import models

from constants import (ADMIN_ROLE, CONFIRMATION_CODE_LENGTH,
                       MAX_USERNAME_LENGTH, MODERATOR_ROLE, USER_ROLE)
from users.validators import regex_validator


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        blank=False,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        blank=False,
        validators=[regex_validator],
    )
    ROLES = (
        (USER_ROLE, 'Пользователь'),
        (MODERATOR_ROLE, 'Модератор'),
        (ADMIN_ROLE, 'Администратор'),
    )
    role = models.CharField(
        max_length=max(len(label) for _, label in ROLES),
        choices=ROLES,
        blank=True,
        null=True,
        default=USER_ROLE,
        verbose_name='Роль'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        verbose_name='Код подтверждения',
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
