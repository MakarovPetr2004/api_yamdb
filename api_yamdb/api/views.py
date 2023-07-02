import random
from string import digits

from api import serializers
from django.core.mail import send_mail
from django.db.models import Avg, PositiveSmallIntegerField
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permission import AdminOrReadOnly, AuthorOrModerOrReadOnly, IsAdminUser
from .serializers import (GetTokenSerializer, UserCreateSerializer,
                          UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.TitleSerializer
    permission_classes = (
        AdminOrReadOnly,
    )
    filterset_class = TitleFilter
    ordering_fields = ['year']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            rating=Avg(
                'reviews__score',
                output_field=PositiveSmallIntegerField()
            )
        )
        return queryset


class BaseClassViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)


class CategoryViewSet(BaseClassViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseClassViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AuthorOrModerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AuthorOrModerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAdminUser,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            data = request.data.copy()
            data.pop('role', None)
            serializer = self.get_serializer(
                request.user,
                data=data,
                partial=True
            )
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    confirmation_code = ''.join(random.choices(digits, k=5))
    serializer.save(confirmation_code=confirmation_code)

    response_status = status.HTTP_200_OK
    response_data = {
        'username': username,
        'email': email,
    }
    send_mail(
        'Код подтверждения для API_YAMDB',
        'Код подтверждения: ' + confirmation_code,
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return Response(response_data, status=response_status)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    user = User.objects.filter(username=username).first()

    if username is None:
        return Response(
            {'detail': 'Поле "username" обязательно'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if user is None:
        return Response(
            {'detail': 'Имя пользователя не найдено'},
            status=status.HTTP_404_NOT_FOUND
        )
    if user.confirmation_code != confirmation_code:
        return Response(
            {'detail': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)
