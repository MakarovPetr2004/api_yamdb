import random
from string import digits

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.permission import IsAdminUser
from users.serializers import UserCreateSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAdminUser,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    confirmation_code = ''.join(random.choices(digits, k=5))
    serializer.save(confirmation_code=confirmation_code)

    response_data = serializer.data
    response_data['confirmation_code'] = confirmation_code

    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    if not username or not confirmation_code:
        return Response(
            'username или confirmation_code отсутствуют в запросе',
            status=status.HTTP_400_BAD_REQUEST
        )

    if not User.objects.filter(username=username).exists():
        return Response(
            'Имя пользователя не найдено',
            status=status.HTTP_404_NOT_FOUND
        )

    user = User.objects.get(username=username)

    if user.confirmation_code != confirmation_code:

        return Response(
            'Неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)})
