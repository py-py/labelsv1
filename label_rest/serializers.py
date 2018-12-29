from rest_framework import serializers
from rest_framework.reverse import reverse

from label.models import *
from label_rest.settings import LABELS_RELATED_SIZE

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
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    added_dt = serializers.SerializerMethodField()
    updated_dt = serializers.SerializerMethodField()
    related_labels = serializers.SerializerMethodField()

    class Meta:
        model = Label
        fields = '__all__'

    def get_added_dt(self, obj):
        return int(obj.added_dt.timestamp() * 1000)

    def get_updated_dt(self, obj):
        return int(obj.updated_dt.timestamp() * 1000)

    def get_url(self, obj):
        url = reverse('label_rest:label-detail', kwargs={'pk': obj.pk})
        return self.context['request'].build_absolute_uri(url)

    def get_image_url(self, obj):
        if obj.default_image:
            return self.context['request'].build_absolute_uri(obj.default_image.image.url)

    def get_related_labels(self, obj):
        related_labels = obj.get_related_labels(LABELS_RELATED_SIZE)
        data = [{
            'id': label.id,
            'image_url': self.context['request'].build_absolute_uri(label.default_image.image.url),
        } for label in related_labels]
        return data
