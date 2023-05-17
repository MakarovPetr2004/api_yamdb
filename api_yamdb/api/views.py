from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api import serializers
from titles.models import Review, User, Title


class TitleViewSet(viewsets.ModelViewSet):
    # Здесь Полина напишет ViewSet для произведений
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        # Здесь Андрей добавит пермишены для отзывов
    )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_title())
