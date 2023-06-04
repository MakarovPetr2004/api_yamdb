import random
from string import digits

from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.permission import IsAdminUser
from users.serializers import (EmailMatchSerializer, GetTokenSerializer,
                               UserCreateSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAdminUser,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            data = request.data.copy()
            data.pop('role', None)
            serializer = self.get_serializer(
                request.user,
                data=data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')

    existing_user = User.objects.filter(username=username).first()

    response_status = status.HTTP_200_OK
    if existing_user:
        serializer = EmailMatchSerializer(
            data=request.data,
            context={'user': existing_user}
        )
        serializer.is_valid(raise_exception=True)
        confirmation_code = ''.join(random.choices(digits, k=5))
        existing_user.confirmation_code = confirmation_code
        existing_user.save()
    else:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = ''.join(random.choices(digits, k=5))
        serializer.save(confirmation_code=confirmation_code)

    response_data = {
        'username': username,
        'email': email,
    }

    send_mail(
        'Код подтверждения для API_YAMDB',
        'Код подтверждения: ' + confirmation_code,
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return Response(response_data, status=response_status)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    token = AccessToken.for_user(user)

    return Response({'token': str(token)})
