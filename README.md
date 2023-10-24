# Foodgram

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Описание
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Шаблон наполнения env-файла,
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY={Ваш секретный ключ}
```

### Запуск приложения в контейнерах
```
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --no-input
```

### Что могут делать неавторизованные пользователи

* Создать аккаунт.
* Просматривать рецепты на главной.
* Просматривать отдельные страницы рецептов.
* Просматривать страницы пользователей.
* Фильтровать рецепты по тегам.

### Что могут делать авторизованные пользователи
* Создать аккаунт.
* Просматривать рецепты на главной.
* Просматривать отдельные страницы рецептов.
* Просматривать страницы пользователей.
* Фильтровать рецепты по тегам.
* Что могут делать авторизованные пользователи
* Входить в систему под своим логином и паролем.
* Выходить из системы (разлогиниваться).
* Менять свой пароль.
* Создавать/редактировать/удалять собственные рецепты
* Просматривать рецепты на главной.
* Просматривать страницы пользователей.
* Просматривать отдельные страницы рецептов.
* Фильтровать рецепты по тегам.
* Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
* Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
* Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

### Что может делать администратор
* Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:
* изменять пароль любого пользователя,
* создавать/блокировать/удалять аккаунты пользователей,
* редактировать/удалять любые рецепты,
* добавлять/удалять/редактировать ингредиенты.
* добавлять/удалять/редактировать теги.
* Все эти функции нужно реализовать в стандартной админ-панели Django.

## Документация
http://practicumvictoria.ddns.net/api/docs/

## Автор
[Федорова Виктория](https://github.com/Victoriafed)
