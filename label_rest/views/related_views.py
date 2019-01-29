from rest_framework import views, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from label.models import *
from label_rest.serializers import *
from label_rest.settings import LABELS_RELATED_SIZE

__all__ = (
    'RelatedLabelAPIView',
)


class RelatedLabelAPIView(views.APIView):
    def get(self, request, id_label):
        try:
            label = Label.objects.get(id=id_label)
        except Label.DoesNotExist as e:
            raise NotFound(detail=e)

        related_labels = label.get_related_labels(LABELS_RELATED_SIZE)
        serializer = RelatedLabelSerializer(
            related_labels,
            many=True,
            context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
