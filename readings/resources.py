from djangorestframework.resources import ModelResource

from readings.models import Reading
from readings.models import CustomerCallLog


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


class CustomerCallLogResource(ModelResource):
    model = CustomerCallLog

    fields = (
        'timestamp',
        'min_latitude',
        'max_latitude',
        'min_longitude',
        'max_longitude',
        'global_data',
        'since_last_call',
        'start_time',
        'end_time',
        'results_limit',
        'data_format',
        'api_key',
        'use_utc',
        'processing_time',
        'results_returned'
    )
