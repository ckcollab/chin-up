import datetime

from django.shortcuts import render

from .models import Metric, MetricRecord


def home(request):
    print 'test'

    return render(request, 'chinup/home.html', {
        'daily_metrics': Metric.objects.filter(daily=True),
        'monthly_metrics': Metric.objects.filter(monthly=True),
    })


def input(request):
    # if form data
    # process form
    # get_or_create each metric + day
    # save data

    return render(request, 'chinup/input.html', {
        'daily_metrics': Metric.objects.filter(daily=True),
        'monthly_metrics': Metric.objects.filter(monthly=True),
        'day_of_month': datetime.date.today().day,
        'date': datetime.date.today()
    })
