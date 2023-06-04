from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='Имя пользователя',
            password='Пароль',
            email='test@mail.ru',
            first_name='Имя',
            last_name='Фамилия'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        user = UserModelTest.user
        field_verboses = {
            'username': 'Логин',
            'password': 'Пароль',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        user = UserModelTest.user
        field_help_texts = {
            'username': 'Введите имя пользователя',
            'password': 'Введите пароль',
            'email': 'Введите почту',
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).help_text, expected_value)
