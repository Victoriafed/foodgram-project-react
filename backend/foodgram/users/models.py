from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=150,
        help_text=('Введите пароль'),
    )
    first_name = models.CharField(
        verbose_name=('Имя'),
        max_length=150,
        help_text=('Введите имя'),
    )
    last_name = models.CharField(
        verbose_name=('Фамилия'),
        max_length=150,
        help_text=('Введите фамилию'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'password',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']
