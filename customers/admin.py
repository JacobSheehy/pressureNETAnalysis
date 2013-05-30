from django.contrib import admin
from customers.models import CustomerPlan, Customer, CustomerCallLog


class CustomerPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'global_calls', 'region_calls', 'regions', 'price')

admin.site.register(CustomerPlan, CustomerPlanAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'company_name', 'contact_mail', 'customer_type')
    list_filter = ('customer_type',)

admin.site.register(Customer, CustomerAdmin)


class CustomerCallLogAdmin(admin.ModelAdmin):
    list_display = ('customer', 'results_returned', 'processing_time', 'timestamp', 'call_type')
    list_filter = ('customer', 'call_type',)

admin.site.register(CustomerCallLog, CustomerCallLogAdmin)
