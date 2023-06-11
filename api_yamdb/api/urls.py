from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

prefix_ver = 'v1/'
prefix_auth = 'auth/'

urlpatterns = [
    path(
        prefix_ver + prefix_auth + 'signup/',
        views.create_user,
        name='create_user'
    ),
    path(
        prefix_ver + prefix_auth + 'token/',
        views.get_token,
        name='get_token'
    ),
    path(prefix_ver, include(router_v1.urls)),
]
