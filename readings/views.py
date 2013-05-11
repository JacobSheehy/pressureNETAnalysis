import urllib2
import time

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json

from djangorestframework.views import ListModelView

from customers.models import Customer, CustomerCallLog
from readings.forms import ReadingForm
from readings.resources import ReadingResource, FullReadingResource
from readings.models import Reading, ReadingSync


def add_from_pressurenet(request):
    """
    Data is incoming from pressureNET.
    Authenticate and add it to the database.
    """
    start = time.time()
    # print request
    # get <-> post with urlencode
    result = urllib2.urlopen('http://ec2-174-129-98-143.compute-1.amazonaws.com:8080/BarometerNetworkServer-3.1/BarometerServlet?pndv=buffer')
    content = result.read()
    readings_list = content.split(';')
    count = 0
    for reading in readings_list:
        raw_location_accuracy = 0
        raw_reading_accuracy = 0
        reading_data = reading.split('|')
        if reading_data[0] == '':
            print 'no data. next reading'
            continue
        raw_latitude = float(reading_data[0])
        raw_longitude = float(reading_data[1])
        raw_reading = float(reading_data[2])
        raw_daterecorded = int(float(reading_data[3]))
        raw_tzoffset = int(float(reading_data[4]))
        raw_user_id = reading_data[5]
        raw_sharing = reading_data[6]
        raw_client_key = reading_data[7]
        try:
            raw_location_accuracy = reading_data[8]
            raw_reading_accuracy = reading_data[9]
        except:
            print 'no accuracy data'
        this_reading = Reading(
            latitude=raw_latitude,
            longitude=raw_longitude,
            reading=raw_reading,
            daterecorded=raw_daterecorded,
            tzoffset=raw_tzoffset,
            user_id=raw_user_id,
            sharing=raw_sharing,
            client_key=raw_client_key,
            location_accuracy=raw_location_accuracy,
            reading_accuracy=raw_reading_accuracy,
        )

        try:
            this_reading.save()
            count += 1
        except:
            continue

    processing_time = time.time() - start
    ReadingSync.objects.create(readings=count, processing_time=processing_time)
    return HttpResponse('okay go, count ' + str(count))


def get_last_api_call_end_time(request_api_key):
    """Return the last API call end time for the given key"""
    call_log = CustomerCallLog.objects.filter(customer__api_key=request_api_key).order_by('-timestamp')[0]
    return call_log.end_time


class IndexView(TemplateView):
    template_name = 'readings/index.html'


class LivestreamView(TemplateView):
    template_name = 'readings/livestream.html'


class AboutView(TemplateView):
    template_name = 'readings/about.html'


class ReadingLiveView(ListModelView):
    """Handle requests for livestreaming"""

    def __init__(self, *args, **kwargs):
        self.call_log = CustomerCallLog()

        super(ReadingLiveView, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        request_api_key = self.request.GET.get('api_key', '')

        if not Customer.objects.filter(api_key=request_api_key).exists():
            return HttpResponseNotAllowed('An API Key is required')

        start = time.time()

        response = super(ReadingLiveView, self).get(*args, **kwargs)

        end = time.time()
        self.call_log.processing_time = end - start
        self.call_log.save()

        return response

    def get_queryset(self):
        # Collect parameters
        request_global_data = self.request.GET.get('global', '')
        request_since_last_call = self.request.GET.get('since_last_call', '')
        # request_use_utc = self.request.GET.get('use_utc', '') # no longer in the API
        request_min_latitude = self.request.GET.get('min_lat', -180)
        request_max_latitude = self.request.GET.get('max_lat', 180)
        request_min_longitude = self.request.GET.get('min_lon', -180)
        request_max_longitude = self.request.GET.get('max_lon', 180)
        request_start_time = self.request.GET.get('start_time', (time.time() - 3600 * 24) * 1000)
        request_end_time = self.request.GET.get('end_time', time.time() * 1000)
        request_results_limit = self.request.GET.get('limit', 1000000)
        request_api_key = self.request.GET.get('api_key', '')
        request_data_format = self.request.GET.get('format', 'json')

        # Figure out the booleans from the strings
        request_global_data = request_global_data.lower() == 'true'
        request_since_last_call = request_since_last_call.lower() == 'true'

        # Perform the query
        # TODO: Ensure sharing privacy matches customer type
        # rather than filter out the Cumulonimbus (Us)
        # Two dynamic parameters request_global_data and
        # since_last_call combine to four distinct queries
        if not (request_global_data or request_since_last_call):
            # Use the start_time and end_time values along with all location parameters
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                latitude__gte=request_min_latitude,
                latitude__lte=request_max_latitude,
                longitude__gte=request_min_longitude,
                longitude__lte=request_max_longitude,
                daterecorded__gte=request_start_time,
                daterecorded__lte=request_end_time,
            ).order_by('user_id').exclude(sharing='Cumulonimbus (Us)')[:request_results_limit]
        elif (request_global_data and request_since_last_call):
            # Check the end time of the last API call with this key
            # And then filter results by that timespan. Globally.
            last_customerapi_call_time = get_last_api_call_end_time(request_api_key)
            # Set the request values for the log
            request_start_time = last_customerapi_call_time
            request_end_time = time.time() * 1000
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                daterecorded__gte=last_customerapi_call_time,
            ).order_by('user_id').exclude(sharing='Cumulonimbus (Us)')[:request_results_limit]
        elif (request_global_data and not request_since_last_call):
            # Return global data for the specified time parameters
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                daterecorded__gte=request_start_time,
                daterecorded__lte=request_end_time,
            ).order_by('user_id').exclude(sharing='Cumulonimbus (Us)')[:request_results_limit]
        elif (request_since_last_call and not request_global_data):
            # Check the end time of the last API call with this key
            # And then filter results by that timespan for the given
            # location parameters.
            last_customerapi_call_time = get_last_api_call_end_time(request_api_key)
            # Set the request values for the log
            request_start_time = last_customerapi_call_time
            request_end_time = time.time() * 1000
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                latitude__gte=request_min_latitude,
                latitude__lte=request_max_latitude,
                longitude__gte=request_min_longitude,
                longitude__lte=request_max_longitude,
                daterecorded__gte=last_customerapi_call_time,
            ).order_by('user_id').exclude(sharing='Cumulonimbus (Us)')[:request_results_limit]

        # Keep a log of this event using CustomerCallLog
        self.call_log.customer = Customer.objects.get(api_key=request_api_key)
        self.call_log.min_latitude = request_min_latitude
        self.call_log.max_latitude = request_max_latitude
        self.call_log.min_longitude = request_min_longitude
        self.call_log.max_longitude = request_max_longitude
        self.call_log.global_data = request_global_data
        self.call_log.since_last_call = request_since_last_call
        self.call_log.start_time = request_start_time
        self.call_log.end_time = request_end_time
        self.call_log.results_limit = request_results_limit
        self.call_log.use_utc = ''
        self.call_log.results_returned = len(queryset)
        self.call_log.data_format = request_data_format

        return queryset


class ReadingListView(ListModelView):

    def get_queryset(self):
        min_lat = self.request.GET.get('minVisLat', None)
        max_lat = self.request.GET.get('maxVisLat', None)
        min_lon = self.request.GET.get('minVisLon', None)
        max_lon = self.request.GET.get('maxVisLon', None)
        start_time = self.request.GET.get('startTime', None)
        end_time = self.request.GET.get('endTime', None)
        limit = self.request.GET.get('limit', None)

        queryset = super(ReadingListView, self).get_queryset().filter(
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lon,
            longitude__lte=max_lon,
            daterecorded__gte=start_time,
            daterecorded__lte=end_time,
        ).order_by('user_id')[:limit]

        return queryset


class CreateReadingView(CreateView):
    model = Reading
    form = ReadingForm

    def form_valid(self, form):
        form.save()
        response = json.dumps({
            'success': True,
            'errors': '',
        })
        return HttpResponse(response, mimetype='application/json')

    def form_invalid(self, form):
        response = json.dumps({
            'success': True,
            'errors': form._errors,
        })
        return HttpResponse(response, mimetype='application/json')


create_reading = csrf_exempt(CreateReadingView.as_view())

index = IndexView.as_view()
livestream = LivestreamView.as_view()
about = AboutView.as_view()
reading_list = ReadingListView.as_view(resource=ReadingResource)
reading_live = ReadingLiveView.as_view(resource=FullReadingResource)
