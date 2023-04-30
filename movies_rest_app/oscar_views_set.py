import django_filters
from django_filters import FilterSet
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .serializers import *


class OscarFilterSet(FilterSet):
    year = django_filters.NumberFilter(field_name='year_awarded', lookup_expr='exact')
    from_year = django_filters.NumberFilter(field_name='year_awarded', lookup_expr='gte')
    to_year = django_filters.NumberFilter(field_name='year_awarded', lookup_expr='lte')
    nomination = django_filters.CharFilter(field_name='nomination', lookup_expr='exact')

    class Meta:
        model = Oscars
        fields = []


class OscarViewSet(ModelViewSet):
    queryset = Oscars.objects.all()
    serializer_class = OscarMovieActorSerializer
    filterset_class = OscarFilterSet

    def get_serializer_class(self):
        if self.action == 'create' and self.request.data['actor'] and self.request.data['nomination_type'] in (
                'best actor in leading role', 'best actor in supporting role', 'best actress in leading role',
                'best actress in supporting role'):
            return OscarActorCreateSerializer
        elif self.action == 'create':
            return OscarCreateSerializer
        else:
            return super().get_serializer_class()

    def filter_queryset(self, queryset):

        queryset = super().filter_queryset(queryset)

        if self.action == 'get_oscars_by_year':
            queryset = queryset.filter(year_awarded=self.kwargs['year_awarded'])

        if self.action in ['list', 'get_oscar_by_year'] and 'actor_nomination' in self.request.query_params and \
                self.request.query_params['actor_nomination'].lower() == 'true':
            queryset = queryset.filter(actor__isnull=False)

        queryset = super().filter_queryset(queryset)

        return queryset

    @action(methods=['GET'], detail=False, url_path=r'years/(?P<year>\d+)$')
    def get_oscars_by_year(self, request, year=None):
        return super().list(request, year_awarded=year)
