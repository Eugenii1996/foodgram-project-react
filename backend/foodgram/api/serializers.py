from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Ingredient, IngredientAmount, Favorite,
    Recipe, RecipeTag, Tag, ShoppingCart
)
from users.serializers import UserSerializer


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        return get_object_or_404(
            obj.ingredientsamount,
            ingredient_id=obj.id, recipe_id=self.context.get('id')
        ).amount


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )
        read_only_fields = ('id', 'author')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Добавьте хотя бы один ингредиент'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными'
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': (
                        'Убедитесь, что значение '
                        'количества ингредиента больше 0'
                    )})
        data['ingredients'] = ingredients
        return data

    def tag_create(self, tags_data, recipe):
        for tag in tags_data:
            new_tag = get_object_or_404(Tag, id=tag.id)
            recipe.tags.add(new_tag)

    def ingredient_create(self, ingredients_data, recipe):
        for ingredient in ingredients_data:
            new_ingredient = IngredientAmount.objects.create(
                ingredient_id=ingredient['id'],
                recipe_id=recipe.id,
                amount=ingredient['amount']
            )
            recipe.ingredients.add(new_ingredient.ingredient_id)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        self.tag_create(tags_data=tags_data, recipe=recipe)
        self.ingredient_create(
            ingredients_data=ingredients_data,
            recipe=recipe
        )
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        tags = list(instance.tags.all())
        if len(tags) > 0:
            RecipeTag.objects.filter(recipe=instance).delete()
        self.tag_create(tags_data=tags_data, recipe=instance)
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.ingredient_create(
            ingredients_data=ingredients_data,
            recipe=instance
        )
        return super(RecipeSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(RecipeSerializer, self).to_representation(instance)
        data['tags'] = TagSerializer(
            instance=instance.tags,
            many=True
        ).data
        return data

    def get_ingredients(self, value):
        ingredient_list = IngredientAmountSerializer(
            value.ingredients.all(),
            many=True,
            read_only=True,
            context={'id': value.id}
        ).data
        return ingredient_list

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user.id
        queryset = Favorite.objects.filter(
            user=request_user, recipes=obj.id
        ).exists()
        return queryset

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user.id
        queryset = ShoppingCart.objects.filter(
            user=request_user, recipes=obj.id
        ).exists()
        return queryset


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)
