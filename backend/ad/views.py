from rest_framework import views, viewsets, serializers
from ad.models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "price",
            "rating",
            "description",
            "date",
        ]


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


