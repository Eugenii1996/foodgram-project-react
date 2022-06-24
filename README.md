# foodgram

### Разработчик:

 - [Мирошниченко Евгений](https://github.com/Eugenii1996)

### О проекте:

Проект Foodgram представляет собой сервис для публикации рецептов приготовления различных блюд и дальнейшего их использования.
Предоставляет клиентам доступ к базе данных.
Данные передаются в формате JSON.
В реализации проекта применена архитектура REST API.
Примененные библиотеки:
 - requests 2.26.0
 - asgiref 3.2.10
 - Django 2.2.16
 - django-filter 2.4.0
 - djangorestframework 3.12.4
 - djangorestframework_simplejwt 5.1.0
 - gunicorn 20.0.4
 - psycopg2-binary 2.8.6
 - PyJWT 2.1.0
 - pytz 2020.1
 - sqlparse 0.3.1
 - pytest 6.2.4
 - pytest-django 4.4.0
 - pytest-pythonpath 0.7.3

### Установка Docker на Windows:

Установите подсистему Linux (WSL2) следуя [инструкции](https://docs.microsoft.com/ru-ru/windows/wsl/install)
Установочный файл можно скачать с [официального сайта](https://www.docker.com/products/docker-desktop/)

### Клонировать репозиторий c GitHub:

```bash
git clone git@github.com:Eugenii1996/foodgram-project-react.git
```

### Шаблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=84.252.137.237
```

### Команды для Docker:

Сборка образа и запуск контейнера выполняется из директории с файлом docker-compose.yaml командой:

```bash
docker-compose up -d
```

Остановить собранные контейнеры и удалить их:

```bash
docker-compose down -v
```

Команды внутри контейнера:

  - Выполнение миграций:

```bash
docker-compose exec web python manage.py migrate
```

  - Создание суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

  - Загрузка статики:

```bash
docker-compose exec web python manage.py collectstatic --no-input 
```

### Ссылка на развернутый и запущенный проект:

http://foodgram.ddnsking.com/ или http://84.252.137.237/

Данные для входа админа:

```
username: admin,
email: admin@yandex.ru,
password: admin
```

### Как наполнить базу данных:

Из дериктории с файлом manage.py выполнить команду:

```bash
ocker-compose exec web python manage.py fill_db_from_csv_files
```