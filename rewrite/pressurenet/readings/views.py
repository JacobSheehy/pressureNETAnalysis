from django.views.generic.base import TemplateView

from djangorestframework.views import ListModelView

from readings.resources import ReadingResource


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
        return super(ReadingListView, self).get_queryset().filter(
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lon,
            longitude__lte=max_lon,
            daterecorded__gte=start_time,
            daterecorded__lte=end_time,
        )[:limit]


index = IndexView.as_view()
reading_list = ReadingListView.as_view(resource=ReadingResource)
