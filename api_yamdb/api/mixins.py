from rest_framework import filters, mixins, viewsets
from .permission import AdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination


class BaseClassViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
