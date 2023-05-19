from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Tag

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
            'color',
            'slug',
        )
