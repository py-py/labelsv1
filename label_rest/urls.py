from django.urls import path
from rest_framework import routers
from .viewsets import *
from .views import *

router = routers.DefaultRouter()
router.register('manufactures', ManufactureViewSet)
router.register('kinds', KindViewSet)
router.register('images', ImageViewSet)
router.register('labels', LabelViewSet)

urlpatterns = router.urls + [
    path('labels/related/<int:id_label>/', RelatedLabelView.as_view(),),
]

