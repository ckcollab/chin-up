import datetime

from datetime import timedelta
from django.db import models


class Metric(models.Model):
    name = models.CharField(max_length=100)
    description_worst = models.TextField(null=True, blank=True)
    description_best = models.TextField(null=True, blank=True)
    daily = models.BooleanField(default=True)
    monthly = models.BooleanField(default=False)
    boolean = models.BooleanField(default=False)

    def how_often_string(self):
        if self.daily:
            return "daily"

        if self.monthly:
            return "monthly"

    def is_boolean_string(self):
        if self.boolean:
            return "boolean"
        else:
            return ""

    def average_span(self, day_span=30):
        avg = MetricRecord.objects.filter(
            metric=self,
            datetime__gt=datetime.datetime.today() - timedelta(days=day_span),
            datetime__lt=datetime.datetime.today()
        ).aggregate(models.Avg('measurement'))

        return avg['measurement__avg']

    def __unicode__(self):
        return "%s (%s) %s" % (self.name, self.how_often_string(), self.is_boolean_string())


class MetricRecord(models.Model):
    metric = models.ForeignKey(Metric, unique_for_date="datetime")
    datetime = models.DateField()
    measurement = models.IntegerField(default=5, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Boolean should default to 0, not 5!
        if self.pk is None and self.metric.boolean:
            self.measurement = 0

        super(MetricRecord, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Record for %s %s on %s" % (self.measurement, self.metric.name, self.datetime)
