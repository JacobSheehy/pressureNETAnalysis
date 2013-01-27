from django.views.generic.base import TemplateView
from djangorestframework.views import ListModelView
from djangorestframework.reverse import reverse
from djangorestframework.response import Response
from readings.resources import ReadingResource
from readings.resources import FullReadingResource
from readings.models import Reading
from django.http import HttpResponse
import urllib2

def add_from_pressurenet(request):
    """
    Data is incoming from pressureNET. 
    Authenticate and add it to the database.
    """
    # print request
    # get <-> post with urlencode
    get_data = [('pndv','buffer'),]     # a sequence of two element tuples
    result = urllib2.urlopen('http://callisto:8080/BarometerNetworkServer-2.2/BarometerServlet?pndv=buffer') #, urllib.urlencode(get_data))
    content = result.read()
    readings_list = content.split(';')
    for reading in readings_list:
      reading_data = reading.split('|')
      raw_latitude = float(reading_data[0])
      raw_longitude = float(reading_data[1])
      raw_reading = float(reading_data[2])
      raw_daterecorded = int(float(reading_data[3]))
      raw_tzoffset = int(float(reading_data[4]))
      raw_user_id = reading_data[5]
      raw_sharing = reading_data[6]
      raw_client_key = reading_data[7]
      this_reading = Reading(
        latitude = raw_latitude,
        longitude = raw_longitude,
        reading = raw_reading,
        daterecorded = raw_daterecorded,
        tzoffset = raw_tzoffset,
        user_id = raw_user_id,
        sharing = raw_sharing,
        client_key = raw_client_key)
      
      this_reading.save()
    return HttpResponse('okay go')


class IndexView(TemplateView):
    template_name = 'readings/index.html'

class ReadingLiveView(ListModelView):
    """Handle requests for livestreaming"""
    def get_queryset(self):
        # Collect parameters
        global_data = self.request.GET.get('global', False)
        min_latitude = self.request.GET.get('min_lat', None)
        max_latitude = self.request.GET.get('max_lat', None)
        min_longitude = self.request.GET.get('min_lon', None)
        max_longitude = self.request.GET.get('max_lon', None)
        start_time = self.request.GET.get('start_time', None)
        end_time = self.request.GET.get('end_time', None)
        since_last_call =  self.request.GET.get('since_last_call', False)
        results_limit = self.request.GET.get('limit', None)
        api_key =  self.request.GET.get('api_key', None)
        use_utc = self.request.GET.get('use_utc', True)

        # Check the API key for validity
        
        
        # Perform the query and return the results
        
        if since_last_call == False:
            # There's no since_last_call, so use the start_time and end_time values
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                latitude__gte=min_latitude,
                latitude__lte=max_latitude,
                longitude__gte=min_longitude,
                longitude__lte=max_longitude,
                daterecorded__gte=start_time,
                daterecorded__lte=end_time,
            ).order_by('user_id') #[:limit]

            return queryset
        else:
            # Find out when this API key made its last call
            # and use that in the query
            pass

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


index = IndexView.as_view()
reading_list = ReadingListView.as_view(resource=ReadingResource)
reading_live = ReadingLiveView.as_view(resource=FullReadingResource)



