# Generated by Django 2.2.19 on 2022-06-18 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_auto_20220615_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcarts', to='recipes.Recipe', verbose_name='Рецепты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcarts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.DeleteModel(
            name='ShopingCart',
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipes'), name='unique_user_recipes'),
        ),
    ]