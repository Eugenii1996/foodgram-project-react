from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .paginations import PageLimitPagination
from .permissions import DeletePatchPutOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer,
    RecipeSerializer, RecipeListSerializer, TagSerializer
)
from recipes.models import (
    Ingredient, IngredientAmount, Tag, Recipe, Favorite, ShoppingCart
)


User = get_user_model()

SHOPPING_LIST_FORMAT = '{name} {measurement_unit} - {total_amount}'
SHOPPING_LIST_FILE_NAME = 'Список покупок'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (DeletePatchPutOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RecipeFilter
    ordering_fields = ('id',)
    ordering = ('-id',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_shopping_cart(
        self,
        request,
        used_model,
        used_serializer,
        id,
        error_message
    ):
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == "POST":
            if_already_exists = used_model.objects.filter(
                user=request.user, recipes=recipe
            ).exists()
            if if_already_exists:
                return Response(
                    {'errors': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            used_model.objects.create(user=request.user, recipes=recipe)
            serializer = used_serializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                used_model,
                user=request.user,
                recipes=recipe
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        error_message = 'Рецепт уже добавлен в избранное'
        return self.favorite_shopping_cart(
            request=request,
            used_model=Favorite,
            used_serializer=FavoriteSerializer,
            id=pk,
            error_message=error_message
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        error_message = 'Рецепт уже добавлен в корзину'
        return self.favorite_shopping_cart(
            request=request,
            used_model=ShoppingCart,
            used_serializer=FavoriteSerializer,
            id=pk,
            error_message=error_message
        )

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = IngredientAmount.objects.filter(
            recipe__shoppingcarts__user=request.user).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(total_amount=Sum('amount'))
        text = '\n'.join([
            SHOPPING_LIST_FORMAT.format(
                name=item['name'],
                measurement_unit=item['measurement_unit'],
                total_amount=item['total_amount']
            )
            for item in shopping_list
        ])
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; '
            f'filename={SHOPPING_LIST_FILE_NAME}'
        )
        return response
