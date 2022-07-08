from django.urls import path, include
from rest_framework import routers

from ad.views import AdViewSet, grab

urlpatterns = [
    path('grab/', grab, name='grab'),
]

router = routers.SimpleRouter()
router.register(r'cars', AdViewSet)
urlpatterns += router.urls


