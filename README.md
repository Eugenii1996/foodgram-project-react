# Продуктовый помощник Foodgram

### Разработчик:

 - [Мирошниченко Евгений](https://github.com/Eugenii1996)

### О проекте:

Проект Foodgram представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Примененные технологии:
 - Python 3
 - Django REST Framework
 - Docker
 - Gunicorn
 - PostgreSQL
 - Git
 - Pytest

### Установка Docker на Windows:

Установите подсистему Linux (WSL2) следуя [инструкции](https://docs.microsoft.com/ru-ru/windows/wsl/install)
Установочный файл можно скачать с [официального сайта](https://www.docker.com/products/docker-desktop/)

### Клонировать репозиторий c GitHub:

```bash
git clone git@github.com:Eugenii1996/foodgram-project-react.git
```

```bash
cd foodgram-project-react
```

### Cоздать и активировать виртуальное окружение:

Виртуальное окружение должно использовать Python 3.7

```bash
pyhton -m venv venv
```

* Если у вас Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

### Установка зависимостей из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
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

Сборка образа и запуск контейнера выполняется из директории с файлом docker-compose.yml командой:

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

### Как наполнить базу данных:

Из дериктории с файлом manage.py выполнить команду:

```bash
docker-compose exec web python manage.py fill_db_from_csv_files
```
