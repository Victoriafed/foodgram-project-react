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
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text=('Введите пароль'),
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
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        ordering = ['-id']


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'author', ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'