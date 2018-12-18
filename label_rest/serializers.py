from rest_framework import serializers
from label.models import *

__all__ = (
    'ManufactureSerializer',
    'KindSerializer',
    'ImageSerializer',
    'LabelSerializer'
)


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufactory
        fields = '__all__'


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Label
        fields = '__all__'
