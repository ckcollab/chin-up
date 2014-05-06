import datetime

from chinup.models import Metric, MetricRecord


daily_metrics = ['Strength', 'Happiness', 'Flexibility', 'Relationships', 'Motiviation', 'Endurance']

for metric_name in daily_metrics:
    metric = Metric.objects.create(name=metric_name, daily=True)
    MetricRecord.objects.create(metric=metric, measurement=7, datetime=datetime.datetime.now())

monthly_metrics = ['Life goals', 'Power', 'Nature']

for metric_name in monthly_metrics:
    metric = Metric.objects.create(name=metric_name, daily=False, monthly=True)
    MetricRecord.objects.create(metric=metric, measurement=7, datetime=datetime.datetime.now())

