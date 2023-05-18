from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, create_user, get_token

from .views import ReviewViewSet, TitleViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('title', TitleViewSet, basename='title')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', create_user, name='create_user'),
    path('v1/auth/token/', get_token, name='get_token'),
]
