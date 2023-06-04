from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator

from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.models import User
from users.validators import UsernameValidationMixin


class UserSerializer(UsernameValidationMixin, serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class UserCreateSerializer(
    UsernameValidationMixin, serializers.ModelSerializer
):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user = User.objects.filter(username=username)
        if user.exists() and user.first().email != email:
            raise serializers.ValidationError(
                'Email does not match the existing user.'
            )

        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise NotFound('Имя пользователя не найдено')

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')

        attrs['user'] = user
        return attrs


class EmailMatchSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = self.context.get('user')

        if user.email != value:
            raise serializers.ValidationError(
                'Email does not match the existing user.'
            )

        return value
