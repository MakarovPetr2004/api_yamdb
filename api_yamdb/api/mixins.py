from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permission import AdminOrReadOnly


class BaseClassViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
