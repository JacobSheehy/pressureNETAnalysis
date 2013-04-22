from django.contrib import admin
from readings.models import Reading, Customer, CustomerCallLog


class ReadingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'latitude', 'longitude', 'reading', 'daterecorded')

admin.site.register(Reading, ReadingAdmin)


class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)


class CustomerCallLogAdmin(admin.ModelAdmin):
    list_display = ('customer', 'results_returned', 'processing_time', 'timestamp')

admin.site.register(CustomerCallLog, CustomerCallLogAdmin)
