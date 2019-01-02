from rest_framework import serializers


__all__ = (
    'RelatedLabelSerializer',
)


class RelatedLabelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.default_image.image.url),
