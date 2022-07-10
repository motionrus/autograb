from django.urls import path, include
from rest_framework import routers

from ad.views import AdViewSet, Grab

urlpatterns = [
    path('grab/', Grab.as_view(), name='grab'),
]

router = routers.SimpleRouter()
router.register(r'cars', AdViewSet)
urlpatterns += router.urls


