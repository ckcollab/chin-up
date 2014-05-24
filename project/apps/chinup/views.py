import datetime
import json

from datetime import timedelta
from dateutil import parser

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render

from .models import Metric, MetricRecord


def append_avg_measurement(metrics, day_span=30):
    combined = []

    for m in metrics:
        avg = MetricRecord.objects.filter(
            metric=m,
            datetime__gt=datetime.datetime.today() - timedelta(days=day_span),
            datetime__lt=datetime.datetime.today()
        ).aggregate(Avg('measurement'))

        combined.append((avg['measurement__avg'], m))

    return combined

def home(request):
    daily_metric_span = int(request.GET.get('daily_metric_span', 30))

    notes = MetricRecord.objects.filter(notes__isnull=False).exclude(notes__exact="")
    notes = notes.values_list('notes', 'datetime').order_by('-datetime')[:10]

    return render(request, 'chinup/home.html', {
        'daily_metric_span': daily_metric_span,
        'daily_metrics': append_avg_measurement(Metric.objects.filter(daily=True, boolean=False), day_span=daily_metric_span),
        'monthly_metrics': append_avg_measurement(Metric.objects.filter(monthly=True, boolean=False), day_span=120),
        'notes': notes,
        }
    )

def input(request):
    date_string = request.GET.get('date', None)

    if date_string is not None and date_string is not '':
        date = parser.parse(date_string)
    else:
        date = datetime.date.today()

    day_of_month = date.day

    metrics = Metric.objects.all()

    if day_of_month != 1:
        # Not first day of month, so filter out monthly
        metrics = Metric.objects.filter(daily=True, monthly=False)

    metric_records = [MetricRecord.objects.get_or_create(datetime=date, metric=m)[0] for m in metrics]
    metric_records_pks = [m.pk for m in metric_records]

    if request.method == "POST":
        data = json.loads(request.body)

        for metric_pk, value in data.items():
            # Make sure we aren't editing something we dont mean to, like if we didnt refresh the page since yesterday
            # it will only be working with datetime=today() by default
            if int(metric_pk) in metric_records_pks:
                for m in metric_records:
                    if m.pk == int(metric_pk):
                        m.notes = value.get('notes', None)
                        m.measurement = value['measurement']
                        m.save()

        return HttpResponse(status=200)

    return render(request, 'chinup/input.html', {
        'daily_checklist': [m for m in metric_records if m.metric.daily and m.metric.boolean],
        'daily_metrics': [m for m in metric_records if m.metric.daily and not m.metric.boolean],
        'monthly_metrics': [m for m in metric_records if m.metric.monthly],
        'day_of_month': day_of_month,
        'date': date,
        'yesterday_link': date - timedelta(days=1),
        'tomorrow_link': date + timedelta(days=1)
    })
