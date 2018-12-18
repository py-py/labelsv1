from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()
router.register('manufactories', ManufactoryViewSet)
router.register('kinds', KindViewSet)
router.register('images', ImageViewSet)
router.register('labels', LabelViewSet)

urlpatterns = router.urls
