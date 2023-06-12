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

auth_urls = [
    path(
        'signup/',
        views.create_user,
        name='create_user'
    ),
    path(
        'token/',
        views.get_token,
        name='get_token'
    ),
]

v1_urls = [
    path('auth/', include(auth_urls)),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls))
]
