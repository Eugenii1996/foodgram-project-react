import csv
from itertools import islice
from django.core.management import BaseCommand

from ...models import Ingredient


class Command(BaseCommand):

    help = 'Импорт баз данных из csv в БД.'

    def handle(self, *args, **kwargs):
        try:
            with open(
                'static/data/ingredients.csv',
                'r',
                encoding='utf-8',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 0, None):
                    _, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],)
            self.stdout.write(
                self.style.SUCCESS(u'Импорт ingredients.csv завершён!'))

        except Exception as error:
            self.stdout.write(self.style.WARNING(error))
