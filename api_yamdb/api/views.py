from api import serializers
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.permission import AdminOrReadOnly, AuthorOrModerOrReadOnly

from .filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.TitleSerializer
    permission_classes = (
        AdminOrReadOnly,
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleSerializer


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.GenreSerializer
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
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

    def create(self, request, *args, **kwargs):
        existing_review = Review.objects.filter(
            title=self.get_title(),
            author=self.request.user
        ).exists()
        if existing_review:
            return Response(
                {'error': 'Вы уже оставили отзыв на это произведение.'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=self.get_title())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


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
