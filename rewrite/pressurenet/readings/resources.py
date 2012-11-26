from djangorestframework.resources import ModelResource

from readings.models import Reading


class ReadingResource(ModelResource):
    model = Reading

    fields = (
        'reading',
        'daterecorded',
    )
