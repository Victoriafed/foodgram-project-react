from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """
        Модель ингредиента.Содержит поля name, measurement_unit.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        db_index=True,
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=30,
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
        Модель тега.Содержит поля name, color, slug.
    """
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=200,
        help_text='Введите название тега'
    )
    color = models.CharField(
        verbose_name='Код цвета',
        unique=True,
        max_length=7,
        help_text='Введите название цвета в формате HEX',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Адрес тега',
        help_text='Введите адрес тега',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
        Модель рецепта.Содержит поля name, author, text, cooking_time,
        ingredients, tags, image.
    """
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Напишите описаниние рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления (более 1 мин)',
        validators=(MinValueValidator(1),)
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        help_text='Выберите теги'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Вставьте изображение блюда',
        upload_to='recipe_img/'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """
        Модель избранное. Связывает пользователя и конкретный рецепт.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранныe рецепты'
        verbose_name_plural = 'Избранныe рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'), name='Unique favorite recipe')
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingСart(models.Model):
    """
        Модель список покупок. Добавляет рецепт в список.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='Unique_shopping_cart')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок'


class RecipeIngredient(models.Model):
    """
        Модель ингредиенты в рецепте. Связывает ингредиенты с рецептом.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='amount',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='amount',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=(MinValueValidator(1),))

    class Meta:
        verbose_name = 'Ингредиенты для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='Unique_ingredient_in_recipe')
        ]
        db_table = 'recipes_recipe_ingredient'

    def __str__(self):
        return (
            f'{self.ingredient.name} - ({self.amount})'
            f'{self.ingredient.measurement_unit} '
        )
