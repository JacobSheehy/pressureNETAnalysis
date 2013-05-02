from django.test import TestCase
from django.core.urlresolvers import reverse

from readings.models import Reading


class CreateReadingTests(TestCase):

    def get_post_data(self):
        return {
            'user_id': 'abc',
            'latitude': 1.0,
            'longitude': 1.0,
            'altitude': 1.0,
            'reading': 1.0,
            'reading_accuracy': 1.0,
            'provider': 'abc',
            'observation_type': 'abc',
            'observation_unit': 'abc',
            'sharing': 'abc',
            'daterecorded': 123,
            'tzoffset': 123,
            'location_accuracy': 1.0,
            'client_key': 'abc',
        }

    def test_create_reading_inserts_into_db(self):
        post_data = self.get_post_data()
        response = self.client.post(reverse('readings-create'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reading.objects.count(), 1)
