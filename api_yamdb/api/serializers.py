from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', 'author')

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Число не находиться в пределах от 1 до 10 включительно.'
            )
        return value
