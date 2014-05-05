import datetime
import qsstats

from django.db.models import Avg
from django.shortcuts import render

from chinup.models import Metric, MetricRecord


def stats_view(request):
    metrics = Metric.objects.all()
    monthly = {}
    weekly = {}
    daily = {}

    for m in metrics:
        measurements = MetricRecord.objects.filter(metric=m)
        monthly[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
            datetime.date.today() - datetime.timedelta(days=365),
            datetime.date.today(),
            aggregate=Avg('measurement'),
            interval='months'
        )

        if not m.monthly:
            weekly[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=365),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='weeks'
            )

            daily[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=365),
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


    earliest_date_recorded = datetime.datetime.today()

    for key, value in monthly.items():
        for entry in value:
            date = entry[0]
            if date < earliest_date_recorded:
                earliest_date_recorded = date


    #import ipdb;ipdb.set_trace()

    # get all metric types
    # get average stats per month
    # get average stats per day (Mon-Sun)


    return render(request, "stats/stats.html", {
        'months_to_ignore': range(1, earliest_date_recorded.month),
        'monthly_measurements': monthly,
        'weekly_measurements': weekly,
        'day_of_week_measurements': daily,
        'metrics': metrics
    })
