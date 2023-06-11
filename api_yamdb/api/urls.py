from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views
from users.views import CurrentUserView, UserViewSet, create_user, get_token

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
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
        create_user,
        name='create_user'
    ),
    path(prefix_ver + prefix_auth + 'token/', get_token, name='get_token'),
    path(prefix_ver + 'users/me/', CurrentUserView.as_view()),
    path(prefix_ver, include(router_v1.urls)),
]
