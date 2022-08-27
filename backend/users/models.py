from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Переопределяем стандартную модель User."""
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким логином уже существует.',
        },
        validators=[
            # RegexValidator(
            #     regex=r'^[a-zA-Z]+[0-9]{0,}+[-_]{0,1}+[a-zA-Z0-9]+$',
            #     message='Не допускаются специальные символы, кроме - или _'
            # )
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Не допустимое имя'
            )
        ],
        verbose_name='Логин',
        help_text='Введите логин пользователя',
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.',
        },
        verbose_name='Email',
        help_text='Введите email пользователя',
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Введите имя пользователя',
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя',
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки на автора рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author',
                ],
                name='unique_follow',
            ),
        ]

    def __str__(self):
        return (f'Пользователь {self.user} '
                f'подписан(а) на автора {self.author}.')
