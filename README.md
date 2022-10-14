# foodgram

### Разработчик:

 - [Мирошниченко Евгений](https://github.com/Eugenii1996)

### О проекте:

Проект Foodgram представляет собой сервис для публикации рецептов приготовления различных блюд и дальнейшего их использования.
Предоставляет клиентам доступ к базе данных.
Данные передаются в формате JSON.
В реализации проекта применена архитектура REST API.
Стек технологий:
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

### Ссылка на развернутый и запущенный проект (В настоящий момент недоступен)):

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
