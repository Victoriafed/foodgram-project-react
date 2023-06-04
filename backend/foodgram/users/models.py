from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        Модель пользователя.Содержит обязательные поля email, username,
        first_name,last_name,password.
    """
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        help_text='Введите имя пользователя'
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Введите пароль'
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
        help_text='Введите почту',
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.',
        }
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text='Введите ваше имя')
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text='Введите вашу фамилию'
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
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """
        Модель подписок.Содержит поля пользователя и автора(пользователя на
        которого подписываются).
    """
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
