from djangorestframework.resources import ModelResource

from readings.models import Reading


class ReadingResource(ModelResource):
    model = Reading

    fields = (
        'reading',
        'daterecorded',
    )

class FullReadingResource(ModelResource):
    model = Reading

    fields = (
        'reading',
        'latitude',
        'longitude',
        'daterecorded',
        'user_id',
        'tzoffset',
        'sharing'
    )
