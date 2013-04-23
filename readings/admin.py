import datetime
import time

from django.contrib import admin
from readings.models import Reading, Customer, CustomerCallLog


class ReadingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'latitude', 'longitude', 'reading', 'daterecorded')

    def changelist_view(self, request, extra_context=None):
        hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        hour_ago = time.mktime(hour_ago.timetuple())
        readings = Reading.objects.filter(daterecorded__gte=(hour_ago*1000)).count()
        context = {
            'readings_per_hour': readings,
        }

        if extra_context:
            context.update(extra_context)

        return super(ReadingAdmin, self).changelist_view(request, context)
        

admin.site.register(Reading, ReadingAdmin)


class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)


class CustomerCallLogAdmin(admin.ModelAdmin):
    list_display = ('customer', 'results_returned', 'processing_time', 'timestamp')

admin.site.register(CustomerCallLog, CustomerCallLogAdmin)
