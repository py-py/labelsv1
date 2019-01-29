from django.contrib.auth.models import User
from rest_framework import generics

from label_rest.serializers import *

__all__ = (
    'UserAPIView',
)


class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
