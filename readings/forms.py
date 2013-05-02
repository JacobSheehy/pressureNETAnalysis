from django import forms

from readings.models import Reading


class ReadingForm(forms.ModelForm):

    class Meta:
        model = Reading
        fields = (
            'user_id',
            'latitude',
            'longitude',
            'altitude',
            'reading',
            'reading_accuracy',
            'provider',
            'observation_type',
            'observation_unit',
            'sharing',
            'daterecorded',
            'tzoffset',
            'location_accuracy',
            'client_key',
        )
