import io

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, Recipe, Tag
from reportlab.pdfgen import canvas
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.models import Favorite, ShoppingCart, IngredientInRecipe
from users.models import Subscription

from .pagination import CustomPagination
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    ShortRecipeSerializer, SubscriptionSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminAuthorOrReadOnly, )

    def get_queryset(self):
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
    def favorite(self, recipe):
        request = self.context.get("request")
        if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
            if request.method == 'DELETE':
                favorite = get_object_or_404(Favorite, user=request.user,
                                           recipe=recipe)
                favorite.delete()
            return Response({'errors': 'Рецепт уже находится в избранном.'},
                                status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        data = ShortRecipeSerializer(recipe)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, recipe):
        request = self.context.get("request")
        if ShoppingCart.objects.filter(recipe=recipe, user=request.user).exists():
            if not request.method == 'DELETE':
                return Response(
                    {'errors': 'Рецепт уже находится в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST)
            shoppingcart = get_object_or_404(Favorite, user=request.user,
                                             recipe=recipe)
            shoppingcart.delete()
        ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
        data = ShortRecipeSerializer(recipe)
        return Response(data, status=status.HTTP_201_CREATED)

    @action()
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        text = (
            f'Список покупок \n'
            f'* {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        )
        p.drawString(100, 100, text)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True,
            filename="shopping_cart.pdf"
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(DjoserViewSet):
    pagination_class = CustomPagination


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Subscription.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
