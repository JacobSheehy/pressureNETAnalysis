from rest_framework import serializers

from readings.models import Reading, Condition


class ReadingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = (
            'reading', 'daterecorded'
        )


class ReadingLiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = (
            'reading',
            'latitude',
            'longitude',
            'daterecorded',
            'user_id',
            'tzoffset',
            'sharing',
            'provider',
            'client_key',
            'location_accuracy',
            'reading_accuracy',
            'observation_type',
            'observation_unit',
        )


class ConditionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'latitude',
            'longitude',
            'altitude',
            'daterecorded',
            'general_condition',
            'windy',
            'fog_thickness',
            'precipitation_type',
            'precipitation_amount',
            'precipitation_unit',
            'thunderstorm_intensity',
            'user_comment',
        )
