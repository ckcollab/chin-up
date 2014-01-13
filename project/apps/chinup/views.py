import datetime
import json

from datetime import timedelta

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render

from .models import Metric, MetricRecord


def append_avg_measurement(metric_list, day_span=30):
    combined = []

    for m in metric_list:
        avg = MetricRecord.objects.filter(metric=m, datetime__gt=datetime.datetime.today() - timedelta(days=day_span)).aggregate(Avg('measurement'))
        combined.append((avg['measurement__avg'], m))

    return combined

def home(request):

    return render(request, 'chinup/home.html', {
        'daily_metrics': append_avg_measurement(Metric.objects.filter(daily=True)),
        'monthly_metrics': append_avg_measurement(Metric.objects.filter(monthly=True), day_span=120),
    })


def input(request):
    day_of_month = datetime.date.today().day
    metrics = Metric.objects.all()

    if day_of_month != 1:
        # First day of month let's do monthly as well, otherwise filter them out
        metrics = Metric.objects.filter(daily=True, monthly=False)

    metric_records = [MetricRecord.objects.get_or_create(datetime=datetime.datetime.today(), metric=m)[0] for m in metrics]
    metric_records_pks = [m.pk for m in metric_records]

    if request.method == "POST":
        data = json.loads(request.POST.items()[0][0])

        for metric_pk, value in data.items():
            # Make sure we aren't editing something we dont mean to, like if we didnt refresh the page since yesterday
            if int(metric_pk) in metric_records_pks:
                for m in metric_records:
                    if m.pk == int(metric_pk):
                        m.measurement = value
                        m.save()

        return HttpResponse(status=200)

    return render(request, 'chinup/input.html', {
        'daily_metrics': [m for m in metric_records if m.metric.daily],
        'monthly_metrics': [m for m in metric_records if m.metric.monthly],
        'day_of_month': day_of_month,
        'date': datetime.date.today(),
    })
