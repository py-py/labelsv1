from rest_framework import viewsets

from label.models import *
from .pagination import LabelPageNumberPagination
from .serializers import *
from .settings import LAST_LABELS_SIZE

__all__ = (
    'ManufactoryViewSet',
    'KindViewSet',
    'ImageViewSet',
    'LabelViewSet',
)


class ManufactoryViewSet(viewsets.ModelViewSet):
    queryset = Manufactory.objects.all()
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
            return queryset[:LAST_LABELS_SIZE]
        return queryset
