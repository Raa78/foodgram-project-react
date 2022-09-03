from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .permissions import (
    IsAuthorOrReadOnly,
    IsReadOnly,
    UserPermission
)
from .serializers import (
    IngredientSerializer,
    RecipeCutSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    SubscribeSerializer,
    TagSerializer,
    UserSerializer,
    SubscribeValidateSerializer,
)
from .utils import make_shopping_list
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscribe, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data['new_password']
        )
        self.request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsReadOnly,)
    filterset_class = IngredientFilter


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_author(self, user_id):
        return get_object_or_404(User, id=user_id)

    def list(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @transaction.atomic()
    def create(self, request, user_id=None):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        data = {
            'user': user.id,
            'author': author.id
        }
        serializer = SubscribeValidateSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.create(
            user=user,
            author=author
        )
        serializer = SubscribeSerializer(
            author,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user_id=None):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        data = {
            'user': user.id,
            'author': author.id
        }
        serializer = SubscribeValidateSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.filter(
            user=user,
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def __get_intersection_model(request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = RecipeCutSerializer(recipe, context={'request': request})
        if request.method == 'POST':
            model.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        model.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.__get_intersection_model(request, pk, Favorite)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.__get_intersection_model(request, pk, ShoppingCart)

    @action(
        detail=False, methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        response = HttpResponse(
            make_shopping_list(request),
            content_type='text/plain; charset=utf8'
        )
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            settings.SHOPPING_CART_FILENAME
            )
        return response
