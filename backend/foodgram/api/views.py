import datetime
import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from reportlab.pdfgen import canvas
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from recipes.models import (
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientInRecipe,
    Ingredient
)
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.models import Subscription
from .pagination import CustomPagination
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    ShortRecipeSerializer,
    SubscriptionSerializer, RecipeReadSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer

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
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
            if request.method == 'DELETE':
                favorite = get_object_or_404(Favorite, user=request.user,
                                             recipe=recipe)
                favorite.delete()
            return Response({'errors': 'Рецепт уже находится в избранном.'},
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        data = ShortRecipeSerializer(recipe)
        return Response(data.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if ShoppingCart.objects.filter(recipe=recipe,
                                       user=request.user).exists():
            if not request.method == 'DELETE':
                return Response(
                    {'errors': 'Рецепт уже находится в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST)
            shoppingcart = get_object_or_404(ShoppingCart, user=request.user,
                                             recipe=recipe)
            shoppingcart.delete()
        ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
        data = ShortRecipeSerializer(recipe)
        return Response(data.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        text = ("jjjjjj"
            """f'Список покупок \n'
            f'* {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients"""
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

    #HHHHH
    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        methods=['POST', 'DELETE']
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
            subscribe = Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if Subscription.objects.filter(user=user, author=author).exists():
            subscribe = get_object_or_404(Subscription, user=user, author=author)
            subscribe.delete()

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        methods=['GET']
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
