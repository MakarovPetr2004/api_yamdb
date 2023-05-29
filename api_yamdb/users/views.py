import random
from string import digits

from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        data = request.data.copy()
        data.pop('role', None)  # remove 'role' from the request data
        serializer = UserSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    existing_user = User.objects.filter(username=username).first()
    response_status = status.HTTP_200_OK
    if existing_user:
        if existing_user.email != email:
            return Response(
                {'error': 'Email does not match the existing user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = ''.join(random.choices(digits, k=5))
        existing_user.confirmation_code = confirmation_code
        existing_user.save()
    else:
        existing_user_email = User.objects.filter(email=email).first()
        if existing_user_email:
            return Response(
                {'error': 'User with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        confirmation_code = ''.join(random.choices(digits, k=5))
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
def createe_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    confirmation_code = ''.join(random.choices(digits, k=5))
    serializer.save(confirmation_code=confirmation_code)
    email = request.data.get('email')

    response_data = serializer.data
    send_mail(
        'Код подтверждения для API_YAMDB',
        'Код подтверждения: ' + confirmation_code,
        'from@example.com',
        [email],
        fail_silently=False,
    )
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
