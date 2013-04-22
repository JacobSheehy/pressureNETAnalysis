from django.contrib import admin
from readings.models import Customer, CustomerCallLog


class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)


class CustomerCallLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'results_returned', 'processing_time')

admin.site.register(CustomerCallLog, CustomerCallLogAdmin)
