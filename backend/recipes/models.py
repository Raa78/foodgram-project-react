from django.core import validators
from django.db import models

from foodgram.settings import (
    COOKING_MIN_TIME,
    COOKING_MIN_TIME_ERROR,
    INGREDIENT_MIN_QUANTITY,
    INGREDIENT_MIN_QUANTITY_ERROR,
)
from users.models import User


class Tag(models.Model):
    """Модель для тэга."""
    name = models.CharField(
        max_length=20,
        unique=True,
        error_messages={
            'unique': 'Данный тэг уже занят другим разделом.',
        },
        verbose_name='Тэг',
        help_text='Введите тэг'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        error_messages={
            'unique': 'Данный цвет уже занят.',
        },
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        error_messages={
            'unique': 'Выбранный slug уже существует.',
        },
        verbose_name='Название тэга',
        help_text='Введите тэг',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'slug',
                ],
                name='unique_slug'),
            models.CheckConstraint(
                name='Нельзя дублировать slug',
                check=~models.Q(name=models.F('slug')),
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингридиентов."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Введите еденицу измерения',
        )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Введите автора рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='Изображение',
        help_text='Добваьте изображение',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Добваьте описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки в минутах',
        validators=(validators.MinValueValidator(
            COOKING_MIN_TIME,
            message=COOKING_MIN_TIME_ERROR),
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (
            f'Рецепт блюда {self.name} '
            f'автор {self.author}')


class IngredientRecipe(models.Model):
    """Модель для ингридиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='consists_of',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='used_in',
        verbose_name='Ингридиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                INGREDIENT_MIN_QUANTITY,
                message=INGREDIENT_MIN_QUANTITY_ERROR),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient',
                ],
                name='unique_recipe_ingredient')
        ]


class Favorite(models.Model):
    """Модель для избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique_favorite')
        ]

    def __str__(self):
        return (
            f'Пользователь {self.user} добавил '
            f'{self.recipe} в избранное.')


class ShoppingCart(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                    ],
                name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'Список покупок пользователя {self.user.username}.'
