import urllib2
    
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from djangorestframework.views import ListModelView
from djangorestframework.reverse import reverse
from djangorestframework.response import Response

from readings.resources import ReadingResource
from readings.resources import FullReadingResource
from readings.models import Reading
from readings.models import CustomerCallLog
from readings.models import Customer

def add_from_pressurenet(request):
    """
    Data is incoming from pressureNET. 
    Authenticate and add it to the database.
    """
    # print request
    # get <-> post with urlencode
    get_data = [('pndv','buffer'),]     # a sequence of two element tuples
    result = urllib2.urlopen('http://ec2-174-129-98-143.compute-1.amazonaws.com:8080/BarometerNetworkServer-3.0/BarometerServlet?pndv=buffer') #, urllib.urlencode(get_data))
    content = result.read()
    readings_list = content.split(';')
    count = 0
    error_message = ''
    for reading in readings_list:
      reading_data = reading.split('|')
      if reading_data[0] == '':
        continue
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
      
      try:
        this_reading.save()
        count += 1
      except:
        continue
    return HttpResponse('okay go, count '+ str(count))


class IndexView(TemplateView):
    template_name = 'readings/index.html'

class ReadingLiveView(ListModelView):
    """Handle requests for livestreaming"""
    def get_queryset(self):
        # Collect parameters
        request_global_data = self.request.GET.get('global', False)
        request_min_latitude = self.request.GET.get('min_lat', None)
        request_max_latitude = self.request.GET.get('max_lat', None)
        request_min_longitude = self.request.GET.get('min_lon', None)
        request_max_longitude = self.request.GET.get('max_lon', None)
        request_start_time = self.request.GET.get('start_time', None)
        request_end_time = self.request.GET.get('end_time', None)
        request_since_last_call =  self.request.GET.get('since_last_call', False)
        request_results_limit = self.request.GET.get('limit', -1)
        request_api_key =  self.request.GET.get('api_key', '')
        request_use_utc = self.request.GET.get('use_utc', True)

        # Figure out the booleans from the strings
        if request_global_data == 'true' or request_global_data == 'True':
            request_global_data = True
        else:
            request_global_data = False
        if request_since_last_call == 'true' or request_since_last_call == 'True':
            request_since_last_call = True
        else:
            request_since_last_call = False        

        # Check the API key for validity
        #api_check = Customer.objects.filter(api_key=request_api_key)
        #if len(api_check) == 0:
            # Not a valid API key. Return an empty queryset. TODO: return an error.
            #queryset = super(ReadingLiveView, self).get_queryset().filter(user_id='-1')
            #return queryset

        if request_api_key not in settings.READINGS_API_KEYS:
            queryset = super(ReadingLiveView, self).get_queryset().filter(user_id='-1')
            return queryset        
       
        # Perform the query
        # TODO: Ensure sharing privacy matches customer type
        if request_since_last_call == False:
            # There's no since_last_call, so use the start_time and end_time values
            queryset = super(ReadingLiveView, self).get_queryset().filter(
                latitude__gte=request_min_latitude,
                latitude__lte=request_max_latitude,
                longitude__gte=request_min_longitude,
                longitude__lte=request_max_longitude,
                daterecorded__gte=request_start_time,
                daterecorded__lte=request_end_time,
            ).order_by('user_id').exclude(sharing='Cumulonimbus (Us)') #[:limit]
        else:
            # Find out when this API key made its last call
            # and use that in the query
            pass
        
        # Keep a log of this event using CustomerCallLog
        """
        TODO: 
        data_format = models.CharField(max_length=10)
        # customer = models.ForeignKey(Customer)
        """
        call_log = CustomerCallLog(
          min_latitude = request_min_latitude,
          max_latitude = request_max_latitude,
          min_longitude = request_min_longitude,
          max_longitude = request_max_longitude,
          global_data = request_global_data,
          since_last_call = request_since_last_call,
          start_time = request_start_time,
          end_time = request_end_time,
          results_limit = request_results_limit,
          api_key = request_api_key,
          use_utc = request_use_utc,
          processing_time = 0,
          results_returned = len(queryset),
          data_format = 'json'
        )
        call_log.save()
        
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


index = IndexView.as_view()
reading_list = ReadingListView.as_view(resource=ReadingResource)
reading_live = ReadingLiveView.as_view(resource=FullReadingResource)

