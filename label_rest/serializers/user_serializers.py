from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

__all__ = (
    'UserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email', 'is_active', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError(_(f'{value} is registered.'))

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
