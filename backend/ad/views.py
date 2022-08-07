from django_rq.utils import get_statistics
from rest_framework import viewsets, serializers, views
from rest_framework.response import Response
from rq.job import Job
from rq.registry import StartedJobRegistry

from ad.models import Ad
from rest_framework import filters

from ad.parser import parse_pages
import django_rq


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
        queue = django_rq.get_queue('high')
        registry = StartedJobRegistry(queue.name, queue.connection)

        if len(registry) == 0 and len(queue) == 0:
            for page in range(1, 101):
                queue.enqueue(parse_pages, page)

        return Response({
            "queued": queue.get_job_ids(),
            "active": registry.get_job_ids(),
        })

    def delete(self, request, *args, **kwargs):
        queue = django_rq.get_queue('high')
        registry = StartedJobRegistry(queue.name, queue.connection)
        if len(registry) > 0:
            job_id = registry.get_job_ids()[0]
            Job.fetch(job_id, connection=queue.connection).delete()

            return Response({"delete": job_id})
        else:
            return Response({"delete": None})

    def get(self, request, *args, **kwargs):
        return Response(get_statistics())
