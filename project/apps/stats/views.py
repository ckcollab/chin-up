import datetime
import qsstats

from django.db.models import Avg
from django.shortcuts import render

from chinup.models import Metric, MetricRecord


def stats_view(request):
    metrics = Metric.objects.all()
    monthly = {}

    for m in metrics:
        measurements = MetricRecord.objects.filter(metric=m)
        monthly[m.name] = qsstats.QuerySetStats(measurements, 'datetime')
        monthly[m.name] = monthly[m.name].time_series(
            datetime.date.today() - datetime.timedelta(days=365),
            datetime.date.today(),
            aggregate=Avg('measurement'),
            interval='months'
        )


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
        'measurements': monthly,
        'metrics': metrics
    })
