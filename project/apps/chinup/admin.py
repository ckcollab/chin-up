from django.contrib import admin

from .models import Metric, MetricRecord


admin.site.register(Metric)
admin.site.register(MetricRecord)
