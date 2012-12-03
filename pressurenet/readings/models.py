from django.db import models


class Reading(models.Model):
    user_id = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    reading = models.FloatField()
    daterecorded = models.BigIntegerField()
    tzoffset = models.BigIntegerField()

    class Meta:
        verbose_name = 'reading'
        verbose_name_plural = 'readings'
        unique_together = ('latitude', 'longitude', 'daterecorded', 'user_id')

    def __unicode__(self):
        return '%s: %s' % (self.user_id, self.reading)
