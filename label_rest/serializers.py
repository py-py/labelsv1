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
    added_dt = serializers.SerializerMethodField()
    updated_dt = serializers.SerializerMethodField()

    class Meta:
        model = Label
        fields = '__all__'

    def get_added_dt(self, obj):
        return int(obj.added_dt.timestamp() * 1000)

    def get_updated_dt(self, obj):
        return int(obj.updated_dt.timestamp() * 1000)
