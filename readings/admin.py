import datetime

from django.core.cache import cache
from django.contrib import admin
from django.utils import simplejson as json

from readings.models import Reading, ReadingSync, Condition
from readings.tests import to_unix


class ReadingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'latitude', 'longitude', 'reading', 'date', 'sharing')
    list_filter = ('sharing',)

    def has_add_permission(self, *args, **kwargs):
        return False

    def changelist_view(self, request, extra_context=None):
        now = datetime.datetime.now()
        current_date = datetime.datetime(now.year, now.month, now.day, now.hour)

        readings_per_hour = []
        for num_hours in range(1, 150):
            start_date = to_unix(current_date - datetime.timedelta(hours=num_hours))
            end_date = to_unix(current_date - datetime.timedelta(hours=(num_hours - 1)))

            cache_key = 'admin:%s:%s' % (start_date, end_date)
            readings = cache.get(cache_key)

            if not readings:
                readings = Reading.objects.all().filter(daterecorded__gte=start_date, daterecorded__lte=end_date).count()
                cache.set(cache_key, readings, 9999999999)

            readings_per_hour.append([end_date, readings])

        active_users_per_hour = []
        for num_hours in range(1, 150):
            start_date = to_unix(current_date - datetime.timedelta(hours=num_hours))
            end_date = to_unix(current_date - datetime.timedelta(hours=(num_hours - 1)))

            cache_key = 'admin:%s:%s' % (start_date, end_date)
            active_users = cache.get(cache_key)

            if not active_users:
                active_users = Reading.objects.all().filter(daterecorded__gte=start_date, daterecorded__lte=end_date).values_list('user_id').distinct().count()
                cache.set(cache_key, active_users, 9999999999)

            active_users_per_hour.append([end_date, active_users])

        context = {
            'readings_data': json.dumps(readings_per_hour),
            'active_user_data': json.dumps(active_users_per_hour),
        }

        if extra_context:
            context.update(extra_context)

        return super(ReadingAdmin, self).changelist_view(request, context)

admin.site.register(Reading, ReadingAdmin)


class ReadingSyncAdmin(admin.ModelAdmin):
    list_display = ('date', 'readings', 'processing_time')

admin.site.register(ReadingSync, ReadingSyncAdmin)


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'latitude', 'longitude', 'general_condition', 'date')

admin.site.register(Condition, ConditionAdmin)
