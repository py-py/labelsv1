from rest_framework import viewsets
from label.models import *
from .serializers import *

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
