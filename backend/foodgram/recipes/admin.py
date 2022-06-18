from django.contrib import admin

from .models import (
    Tag, Ingredient, IngredientAmount, Recipe,
    RecipeTag, ShoppingCart, Favorite, Follow
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'favorits',
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'

    def favorits(self, obj):
        return obj.favorits.count()

    favorits.short_description = 'Количество добавлений в избранное'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
