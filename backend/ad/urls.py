from rest_framework import routers

from ad.views import AdViewSet

router = routers.SimpleRouter()
router.register(r'ads', AdViewSet)
urlpatterns = router.urls
