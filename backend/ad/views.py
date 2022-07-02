import django_filters
from rest_framework import views, viewsets, serializers
from ad.models import Ad

from rest_framework import filters


class Ordering(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):

        ordering = self.get_ordering(request, queryset, view)

        if not ordering:
            return queryset

        if '-rating' in ordering:
            return sorted(queryset, key=lambda t: -t.rating_number)
        if 'rating' in ordering:
            return sorted(queryset, key=lambda t: t.rating_number)

        return queryset.order_by(*ordering)


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "price",
            "rating",
            "description",
            "updated_at",
            "url",
        ]


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [Ordering]
    ordering_fields = ('name', 'price', 'rating', 'updated_at')
