from django.db.models import F
from rest_framework import viewsets

from label.models import *
from .pagination import LabelPageNumberPagination
from .serializers import *
from .settings import LABELS_LAST_SIZE

__all__ = (
    'ManufactureViewSet',
    'KindViewSet',
    'ImageViewSet',
    'LabelViewSet',
)


class ManufactureViewSet(viewsets.ModelViewSet):
    queryset = Manufacture.objects.all()
    serializer_class = ManufactureSerializer


class KindViewSet(viewsets.ModelViewSet):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = LabelPageNumberPagination

    def get_queryset(self):
        queryset = super(LabelViewSet, self).get_queryset()
        queryset = queryset.order_by('-updated_dt')
        if 'last' in self.request.query_params:
            return queryset[:LABELS_LAST_SIZE]
        return queryset

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        instance.seen = F('seen') + 1
        instance.save()
        return super(LabelViewSet, self).retrieve(*args, **kwargs)
