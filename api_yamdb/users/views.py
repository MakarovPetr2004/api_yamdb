import random
from string import digits

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    confirmation_code = ''.join(random.choices(digits, k=5))
    serializer.save(confirmation_code=confirmation_code)

    response_data = serializer.data
    response_data['confirmation_code'] = confirmation_code

    return Response(response_data)
