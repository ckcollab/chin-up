import datetime
import qsstats

from django.db.models import Avg
from django.shortcuts import render

from chinup.models import Metric, MetricRecord


class StatsView(object):

    def __init__(self, request, *args, **kwargs):
        self.request = request

        if MetricRecord.objects.exists():
            self.metrics = Metric.objects.filter(boolean=False)
            self.days = int(request.GET.get('days', 365))
            self.earliest_recorded_entry = MetricRecord.objects.all().order_by('datetime')[:1][0]
            self.max_days = datetime.datetime.now().date() - self.earliest_recorded_entry.datetime

            if self.days > self.max_days.days:
                self.days = self.max_days.days

            self.no_measurements_yet = False
        else:
            self.no_measurements_yet = True

    def get_week_long_averages(self):
        weekly = {}

        for m in self.metrics:
            if not m.monthly:
                measurements = MetricRecord.objects.filter(metric=m)
                weekly[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                    datetime.date.today() - datetime.timedelta(days=self.days),
                    datetime.date.today(),
                    aggregate=Avg('measurement'),
                    interval='weeks'
                )

        return weekly

    def get_month_long_averages(self):
        monthly = {}

        for m in self.metrics:
            month_query = MetricRecord.objects.filter(metric=m, measurement__gt=0)
            monthly[m.name] = qsstats.QuerySetStats(month_query, 'datetime').time_series(
                datetime.date.today() - datetime.timedelta(days=self.days),
                datetime.date.today(),
                aggregate=Avg('measurement'),
                interval='months'
            )

        return monthly

    def get_day_of_week_averages(self):
        daily = {}

        for m in self.metrics:
            if not m.monthly:
                measurements = MetricRecord.objects.filter(metric=m)
                daily[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                    datetime.date.today() - datetime.timedelta(days=self.days),
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

                if len(days_of_week[day]) - zeroes:
                    calc = float(total / (len(days_of_week[day]) - zeroes))
                else:
                    calc = 0.0

                days_of_week[day] = (None, calc)

            daily[key] = [v for d, v in days_of_week.items()]

        return daily

    def get_last_7_day_averages(self):
        last_7_days = {}

        for m in self.metrics:
            if not m.monthly:
                measurements = MetricRecord.objects.filter(metric=m)
                last_7_days[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                    datetime.date.today() - datetime.timedelta(days=6),
                    datetime.date.today(),
                    aggregate=Avg('measurement'),
                    interval='days'
                )

        return last_7_days

    def get_last_30_day_averages(self):
        last_30_days = {}

        for m in self.metrics:
            if not m.monthly:
                measurements = MetricRecord.objects.filter(metric=m)
                last_30_days[m.name] = qsstats.QuerySetStats(measurements, 'datetime').time_series(
                    datetime.date.today() - datetime.timedelta(days=30),
                    datetime.date.today(),
                    aggregate=Avg('measurement'),
                    interval='days'
                )

        return last_30_days

    def get_months_on_y_axis(self):
        all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        months_y_axis = []

        for month_number in range(self.earliest_recorded_entry.datetime.month, datetime.datetime.today().month + 1):
            months_y_axis.append(all_months[month_number - 1])

        return months_y_axis

    def get_last_7_day_names(self, last_7_days):
        last_7_day_names = []
        day_names = ['Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat']

        for metric_record in last_7_days[last_7_days.keys()[0]]:
            # For some reason the day is one behind, adjuuust
            day_adjusted = (metric_record[0] + datetime.timedelta(days=1)).isoweekday() - 1
            last_7_day_names.append(day_names[day_adjusted])

        return last_7_day_names

    def get_context(self):
        if not self.no_measurements_yet:
            # Save this one to calculate the last 7 day names
            last_7_days = self.get_last_7_day_averages()

            return render(self.request, "stats/stats.html", {
                'months_y_axis': self.get_months_on_y_axis(),
                'monthly_measurements': self.get_month_long_averages(),
                'weekly_measurements': self.get_week_long_averages(),
                'day_of_week_measurements': self.get_day_of_week_averages(),
                'metrics': self.metrics,
                'last_7_days': last_7_days,
                'last_30_days': self.get_last_30_day_averages(),
                'last_7_day_names': self.get_last_7_day_names(last_7_days)
            })
        else:
            return render(self.request, "stats/stats.html", {
                'no_measurements_yet': True
            })


def stats_view(request):
    return StatsView(request).get_context()
