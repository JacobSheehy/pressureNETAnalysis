from djangorestframework.resources import ModelResource

from readings.models import Reading, Condition


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
        'sharing',
        'client_key',
        'location_accuracy',
        'reading_accuracy',
    )


class ConditionResource(ModelResource):
    model = Condition
    fields = (
        'user_id',
        'latitude',
        'longitude',
        'altitude',
        'daterecorded',
        'tzoffset',
        'accuracy',
        'provider',
        'sharing',
        'client_key',
        'general_condition',
        'windy',
        'fog_thickness',
        'precipitation_type',
        'precipitation_amount',
        'precipitation_unit',
        'thunderstorm_intensity',
        'user_comment',
    )
