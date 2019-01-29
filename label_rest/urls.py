from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .viewsets import *
from .views import *

router = routers.DefaultRouter()
router.register('manufactures', ManufactureViewSet)
router.register('kinds', KindViewSet)
router.register('images', ImageViewSet)
router.register('labels', LabelViewSet)

urlpatterns = router.urls + [
    path('auth/obtain/', obtain_jwt_token),
    path('auth/refresh/', refresh_jwt_token),
    path('auth/verify/', verify_jwt_token),

    path('users/', UserAPIView.as_view(), ),
    path('labels/related/<int:id_label>/', RelatedLabelAPIView.as_view(), ),
]

