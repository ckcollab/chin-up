from django.db import models


class Metric(models.Model):
    name = models.CharField(max_length=100)
    description_worst = models.TextField()
    description_best = models.TextField()
    daily = models.BooleanField(default=True)
    monthly = models.BooleanField(default=False)

    def how_often_string(self):
        if self.daily:
            return "daily"

        if self.monthly:
            return "monthly"

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.how_often_string())


class MetricRecord(models.Model):
    metric = models.ForeignKey(Metric, unique_for_date="datetime")
    datetime = models.DateField()
    measurement = models.IntegerField(default=5, blank=True)
    notes = models.TextField()

    def __unicode__(self):
        return "Record for %s %s on %s" % (self.measurement, self.metric.name, self.datetime)
