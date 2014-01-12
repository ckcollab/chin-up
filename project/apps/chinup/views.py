from django.shortcuts import render

from .models import Metric, MetricRecord


def home(request):
    print 'test'

    return render(request, 'chinup/home.html', {
        'daily_metrics': Metric.objects.filter(daily=True),
        'monthly_metrics': Metric.objects.filter(monthly=True),
    })


def input(request):
    return render(request, 'chinup/input.html', {})
