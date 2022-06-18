from csv import DictReader
from django.core.management import BaseCommand

from ...models import Ingredient, Tag


ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно заново загрузить данные из CSV файла,
сначала удалите файл db.sqlite3 для очистки базы данных.
Затем выполните команду `python manage.py migrate` для создания новой
пустой базы данных"""


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Показать это сообщение,
        # если данные об ингредиенте уже есть в базе данных
        if Ingredient.objects.exists():
            print('Данные об ингредиенте уже существуют.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Показать это сообщение перед началом загрузки данных
        print("Загрузка информации об ингредиентах")

        # Загрузка ингредиентов
        for row in DictReader(open('../../data/ingredients.csv')):
            ingredient = Ingredient(
                name=row['Name'],
                measurement_unit=row['Measurement_unit']
            )
            ingredient.save()

        # Загрузка тегов
        for row in DictReader(open('../../data/tags.csv')):
            ingredient = Tag(
                name=row['Name'],
                color=row['Color'],
                slug=row['Slug']
            )
            ingredient.save()
