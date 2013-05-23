from django.conf import settings

import django_filters

from readings.models import Reading, Condition


class DateLocationFilterSet(django_filters.FilterSet):
    min_latitude = django_filters.NumberFilter(name='latitude', lookup_type='gte')
    max_latitude = django_filters.NumberFilter(name='latitude', lookup_type='lte')
    min_longitude = django_filters.NumberFilter(name='longitude', lookup_type='gte')
    max_longitude = django_filters.NumberFilter(name='longitude', lookup_type='lte')
    start_time = django_filters.NumberFilter(name='daterecorded', lookup_type='gte')
    end_time = django_filters.NumberFilter(name='daterecorded', lookup_type='lte')
    limit = django_filters.NumberFilter(action=lambda queryset, limit: queryset[:limit])

    @property
    def qs(self):
        return super(DateLocationFilterSet, self).qs[:settings.MAX_CALL_LENGTH]


class ReadingListFilter(DateLocationFilterSet):

    class Meta:
        model = Reading
        fields = (
            'min_latitude',
            'max_latitude',
            'min_longitude',
            'max_longitude',
            'start_time',
            'end_time',
            'limit',
        )


class ConditionListFilter(DateLocationFilterSet):

    class Meta:
        model = Condition
        fields = (
            'min_latitude',
            'max_latitude',
            'min_longitude',
            'max_longitude',
            'start_time',
            'end_time',
            'limit',
        )
