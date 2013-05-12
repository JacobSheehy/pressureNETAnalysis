from django.contrib import admin
from customers.models import Customer, CustomerCallLog


class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)


class CustomerCallLogAdmin(admin.ModelAdmin):
    list_display = ('customer', 'results_returned', 'processing_time', 'timestamp', 'call_type')
    list_filter = ('customer', 'call_type',)

admin.site.register(CustomerCallLog, CustomerCallLogAdmin)
