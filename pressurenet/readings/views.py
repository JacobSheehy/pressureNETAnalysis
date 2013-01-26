from django.views.generic.base import TemplateView
from djangorestframework.views import ListModelView
from djangorestframework.reverse import reverse
from djangorestframework.response import Response
from pressurenet.readings.resources import ReadingResource
from django.http import HttpResponse
import urllib2
from readings.models import Reading

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
    print 'processing', len(readings_list), 'readings'
    for reading in readings_list:
      reading_data = reading.split(',')
      raw_latitude = float(reading_data[0])
      raw_longitude = float(reading_data[1])
      raw_reading = float(reading_data[2])
      raw_daterecorded = int(float(reading_data[3]))
      raw_tzoffset = int(float(reading_data[4]))
      raw_user_id = reading_data[5]
      raw_sharing = reading_data[6]
      this_reading = Reading(
        latitude = raw_latitude,
        longitude = raw_longitude,
        reading = raw_reading,
        daterecorded = raw_daterecorded,
        tzoffset = raw_tzoffset,
        user_id = raw_user_id,
        sharing = raw_sharing)
      
      this_reading.save()
      print 'saved', raw_reading 
    #print readings_list
    return HttpResponse('okay go')


class IndexView(TemplateView):
    template_name = 'readings/index.html'

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
