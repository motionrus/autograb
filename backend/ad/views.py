from rest_framework import viewsets, serializers, views
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ad.job import SingleTonJob
from ad.models import Ad
from rest_framework import filters
import django_rq
from django.core.management import call_command

from ad.parser import PaginationParser


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


class Grab(views.APIView):
    def post(self, request, *args, **kwargs):
        job = SingleTonJob().get_job()
        return Response({"updated": job.id})

    def get(self, request, *args, **kwargs):
        print(SingleTonJob().percentage)
        return Response({"url": "", "percentage": SingleTonJob().percentage})
