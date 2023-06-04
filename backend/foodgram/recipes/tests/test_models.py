from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import Ingredient, Tag, Recipe, Favorite

User = get_user_model()


class IngredientModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredient = Ingredient.objects.create(
            name='Название ингредиента',
            measurement_unit='Единица измерения'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        ingredient = IngredientModelTest.ingredient
        field_verboses = {
            'name': 'Название ингредиента',
            'measurement_unit': 'Единица измерения',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    ingredient._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        ingredient = IngredientModelTest.ingredient
        field_help_texts = {
            'name': 'Введите название ингредиента',
            'measurement_unit': 'Введите единицу измерения',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    ingredient._meta.get_field(field).help_text, expected_value)


class TagModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create(
            name='Название',
            color='Код цвета',
            slug='Адрес тега'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        tag = TagModelTest.tag
        field_verboses = {
            'name': 'Название',
            'color': 'Код цвета',
            'slug': 'Адрес тега'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    tag._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        tag = TagModelTest.tag
        field_help_texts = {
            'name': 'Введите название тега',
            'color': 'Введите название цвета в формате HEX',
            'slug': 'Введите адрес тега'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    tag._meta.get_field(field).help_text, expected_value)


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.recipe = Recipe.objects.create(
            name='Название рецепта',
            author='Автор',
            text='Описание рецепта',
            cooking_time='Время приготовления',
            ingredients='Ингредиенты',
            tags='Теги',
            image='Изображение',
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        recipe = RecipeModelTest.recipe
        field_verboses = {
            'name': 'Название рецепта',
            'author': 'Автор',
            'text': 'Описание рецепта',
            'cooking_time': 'Время приготовления',
            'ingredients': 'Ингредиенты',
            'tags': 'Теги',
            'image': 'Изображение',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        recipe = RecipeModelTest.recipe
        field_help_texts = {
            'name': 'Введите название рецепта',
            'text': 'Напишите описаниние рецепта',
            'cooking_time': 'Введите время приготовления (более 1 мин)',
            'ingredients': 'Выберите ингредиенты',
            'tags': 'Выберите теги',
            'image': 'Вставьте изображение блюда',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe._meta.get_field(field).help_text, expected_value)
