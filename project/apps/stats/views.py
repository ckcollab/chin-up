import datetime
import qsstats
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db.models import Avg
from django.shortcuts import render

from chinup.models import Metric, MetricRecord


def stats_view(request):
    days = int(request.GET.get('days', 365))

    metrics = Metric.objects.all()
    monthly = {}
    weekly = {}
    daily = {}
    last_7_days = {}
    last_30_days = {}


    if MetricRecord.objects.exists():
        earliest_recorded_entry = MetricRecord.objects.all().order_by('datetime')[:1][0]

        max_days = datetime.date.today() - earliest_recorded_entry.datetime

        if days > max_days.days:
            days = max_days.days

        print earliest_recorded_entry
    else:
        return render(request, "stats/stats.html", {
            'error': 'Please add at least a <a href="%s">Metric</a> and <a href="../input/">enter some Metric records</a>.' % reverse('admin:chinup_metric_add')
        })

    for m in metrics:
        month_query = MetricRecord.objects.filter(metric=m, measurement__gt=0)
        monthly[m.name] = qsstats.QuerySetStats(month_query, 'datetime').time_series(
            datetime.date.today() - datetime.timedelta(days=days),
            datetime.date.today(),
            aggregate=Avg('measurement'),
            interval='months'
        )

        if not m.monthly:
            measurements = MetricRecord.objects.filter(metric=m)

            weekly[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=days),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='weeks'
            )

            daily[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=days),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='days'
            )

            last_7_days[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=6),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='days'
            )

            last_30_days[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=30),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='days'
            )

    for key, value in daily.items():
        days_of_week = {'7': []}
        for i in range(1, 7):
            days_of_week[str(i)] = []

        for measurement in value:
            days_of_week[str(measurement[0].isoweekday())].append(measurement)

        for day, measurements in days_of_week.items():
            total = sum([r[1] for r in days_of_week[day]])

            zeroes = 0

            for i in days_of_week[day]:
                if i[1] < 1:
                    zeroes += 1

            days_of_week[day] = (None, float(total / (len(days_of_week[day]) - zeroes)))

        daily[key] = [v for d, v in days_of_week.items()]

    all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    months_y_axis = []

    for month_number in range(earliest_recorded_entry.datetime.month, datetime.datetime.today().month + 1):
        months_y_axis.append(all_months[month_number - 1])

    last_7_day_names = []
    day_names = ['Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat']

    for metric_record in last_7_days[last_7_days.keys()[0]]:
        # For some reason the day is one behind, adjuuust
        day_adjusted = (metric_record[0] + datetime.timedelta(days=1)).isoweekday() - 1
        last_7_day_names.append(day_names[day_adjusted])

    return render(request, "stats/stats.html", {
        'months_y_axis': months_y_axis,
        'monthly_measurements': monthly,
        'weekly_measurements': weekly,
        'day_of_week_measurements': daily,
        'metrics': metrics,
        'last_7_days': last_7_days,
        'last_30_days': last_30_days,
        'last_7_day_names': last_7_day_names
    })
