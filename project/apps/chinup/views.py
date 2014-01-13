import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Metric, MetricRecord


def home(request):

    return render(request, 'chinup/home.html', {
        'daily_metrics': Metric.objects.filter(daily=True),
        'monthly_metrics': Metric.objects.filter(monthly=True),
    })


def input(request):
    # get_or_create each metric + day
    metrics = Metric.objects.all()

    metric_records = [MetricRecord.objects.get_or_create(datetime=datetime.datetime.today(), metric=m)[0] for m in metrics]
    metric_records_pks = [m.pk for m in metric_records]
    # if form data
    #   process form
    #   save data to metrics
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
        'day_of_month': datetime.date.today().day,
        'date': datetime.date.today(),
    })
