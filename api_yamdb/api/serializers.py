import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.models import User
from users.validators import UsernameValidationMixin


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )
        read_only_fields = ('rating',)

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        return representation


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Число не находиться в пределах от 1 до 10 включительно.'
            )
        return value

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(Title, pk=title_id)

            if Review.objects.filter(author=user, title=title).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )


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

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')

        user = User.objects.create(username=username, email=email)

        return user


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


