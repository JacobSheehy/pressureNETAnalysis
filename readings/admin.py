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
        readings_per_day = []
        for num_days in range(1, 20):
            start_date = to_unix(datetime.date.today() - datetime.timedelta(days=num_days))
            end_date = to_unix(datetime.date.today() - datetime.timedelta(days=(num_days - 1)))

            cache_key = 'admin:%s:%s' % (start_date, end_date)
            readings = cache.get(cache_key)

            if not readings:
                readings = Reading.objects.all().filter(daterecorded__gte=start_date, daterecorded__lte=end_date).count()
                cache.set(cache_key, readings, 9999999999)

            readings_per_day.append([end_date, readings])

        active_users = []
        for num_days in range(1, 20):
            start_date = to_unix(datetime.date.today() - datetime.timedelta(days=num_days))
            end_date = to_unix(datetime.date.today() - datetime.timedelta(days=(num_days - 1)))

            cache_key = 'admin:%s:%s' % (start_date, end_date)
            users = cache.get(cache_key)

            if not users:
                users = Reading.objects.all().filter(daterecorded__gte=start_date, daterecorded__lte=end_date).values_list('user_id').distinct().count()
                cache.set(cache_key, users, 9999999999)

            active_users.append([end_date, users])

        context = {
            'readings_data': json.dumps(readings_per_day),
            'active_user_data': json.dumps(active_users),
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
