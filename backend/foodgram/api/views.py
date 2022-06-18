from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .paginations import PageLimitPagination
from .permissions import IsOwner
from .serializers import (
    FavoriteSerializer, IngredientSerializer,
    RecipeSerializer, TagSerializer
)
from recipes.models import (
    Ingredient, Tag, Recipe, Favorite, ShoppingCart
)


User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = RecipeFilter
    ordering_fields = ('id',)
    ordering = ('-id',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update', 'update']:
            return (IsOwner(),)
        return super().get_permissions()

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if_already_exists = Favorite.objects.filter(
                user=request.user, recipes=recipe
            ).exists()
            if if_already_exists or request.user == recipe.author:
                return Response({
                    'errors': ('Рецеапт уже добавлен в '
                               'избранное или это ваш рецепт')
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=request.user, recipes=recipe)
            serializer = FavoriteSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Favorite,
                user=request.user,
                recipes=recipe
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if_already_exists = ShoppingCart.objects.filter(
                user=request.user,
                recipes=recipe
            ).exists()
            if if_already_exists:
                return Response({
                    'errors': 'Рецепт уже добавлен в корзину'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=request.user, recipes=recipe)
            serializer = FavoriteSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipes=recipe
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        recipe_list = Recipe.objects.filter(
            shoppingcarts__user=self.request.user)
        serializer = RecipeSerializer(
            recipe_list, context={'request': request}, many=True)
        ingredients_list = []
        for recipe in serializer.data:
            for ingredient in recipe['ingredients']:
                for i in ingredients_list:
                    if ingredient['id'] == i['id']:
                        i['amount'] += ingredient['amount']
                if ingredient not in ingredients_list:
                    ingredients_list.append(ingredient)
        shopping_cart = []
        for ing in ingredients_list:
            name = ing['name'].capitalize()
            measure = ing['measurement_unit']
            amount = ing['amount']
            shopping_cart.append(f"{name} ({measure}) - {amount}")
        return Response(shopping_cart,  content_type='text/plain')
