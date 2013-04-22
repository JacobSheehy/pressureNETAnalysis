from django.db import models


class Reading(models.Model):
    """Barometer reading from pressureNET"""
    user_id = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    reading = models.FloatField()
    daterecorded = models.BigIntegerField()
    tzoffset = models.BigIntegerField()
    sharing = models.CharField(max_length=255)
    client_key = models.CharField(max_length=255)
    location_accuracy = models.FloatField()
    reading_accuracy = models.FloatField()

    class Meta:
        verbose_name = 'reading'
        verbose_name_plural = 'readings'
        unique_together = ('latitude', 'longitude', 'daterecorded', 'user_id')

    def __unicode__(self):
        return '%s: %s' % (self.user_id, self.reading)


class Customer(models.Model):
    """Customer data"""
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_mail = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=25, blank=True, null=True)
    contact_address = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    payment_confirmation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        unique_together = ('company_name', 'contact_name', 'contact_mail')
    
    def __unicode__(self):
        return '%s: %s' % (self.company_name, self.contact_mail)


class CustomerCallLog(models.Model):
    """Log data for each customer API call"""
    timestamp = models.DateTimeField(auto_now_add=True)
    min_latitude = models.FloatField()
    max_latitude = models.FloatField()
    min_longitude = models.FloatField()
    max_longitude = models.FloatField()
    global_data = models.BooleanField()
    since_last_call = models.BooleanField()
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    results_limit = models.IntegerField()
    data_format = models.CharField(max_length=10)
    api_key = models.CharField(max_length=255)
    use_utc = models.BooleanField()
    processing_time = models.FloatField()
    results_returned = models.IntegerField()

    class Meta:
        verbose_name = 'customercalllog'
        verbose_name_plural = 'customercalllogs'
        unique_together = ('timestamp','api_key')
    
    def __unicode__(self):
        return '%s: %s %s' % (self.timestamp, self.results_returned, self.api_key) 
