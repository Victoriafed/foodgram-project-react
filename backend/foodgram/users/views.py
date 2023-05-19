from rest_framework import viewsets

from api.serializers import UsersSerializer

from .models import User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    search_fields = ('username',)
