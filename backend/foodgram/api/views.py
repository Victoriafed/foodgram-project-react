import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingСart, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeModifySerializer,
                          RecipeSerializer, RecipeSubscribeSerializer,
                          TagSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    """
        View для ингредиентов
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    """
        View для тегов
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class RecipeViewSet(viewsets.ModelViewSet):
    """
        View для рецептов
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """
            Возвращает необходимый serializer
        """
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeModifySerializer

    def get_queryset(self):
        """
            Возвращает список рецептов
        """
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(favorites__user=self.request.user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return Recipe.objects.all()

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """
            Метод для работы со списком покупок
        """
        if request.method == 'POST':
            return self.add_to(ShoppingСart, request.user, pk)
        return self.delete_from(ShoppingСart, request.user, pk)

    @staticmethod
    def add_to(model, user, pk):
        """
            Метод для добовления
        """
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSubscribeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from(model, user, pk):
        """
            Метод для удаления
        """
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        """
            Метод для работы с избранным
        """
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        return self.delete_from(Favorite, request.user, pk)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """
            Метод позвляющий загружать список покупок
        """
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.date.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
