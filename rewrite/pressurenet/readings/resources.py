from django.conf import settings
from django.utils import translation

from djangorestframework.resources import ModelResource

from readings.models import Reading


class ReadingResource(ModelResource):
    model = Reading

    fields = (
        'latitude',
        'longitude',
        'reading',
        'daterecorded',
        'tzoffset',
    )
