from rest_framework import serializers
from rest_framework.reverse import reverse

from label.models import *

__all__ = (
    'ManufactureSerializer',
    'KindSerializer',
    'ImageSerializer',
    'LabelSerializer'
)


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacture
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
    images = ImageSerializer(many=True, read_only=True)  # using 2 requests;
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    added_ts = serializers.SerializerMethodField()
    updated_ts = serializers.SerializerMethodField()

    class Meta:
        model = Label
        fields = '__all__'
        extra_kwargs = {
            'kind': {'required': True},
            'manufacture': {'required': True},
        }

    def get_added_ts(self, obj):
        return int(obj.added_dt.timestamp() * 1000)

    def get_updated_ts(self, obj):
        return int(obj.updated_dt.timestamp() * 1000)

    def get_url(self, obj):
        url = reverse('label_rest:label-detail', kwargs={'pk': obj.pk})
        return self.context['request'].build_absolute_uri(url)

    def get_image_url(self, obj):
        if obj.default_image:
            return self.context['request'].build_absolute_uri(obj.default_image.image.url)

