from numpy import corrcoef

from django.shortcuts import render

from chinup.models import Metric, MetricRecord


def correlation_view(request):
    # Get all metric names and data
    metric_objects = Metric.objects.filter(daily=True).values_list('name')
    metric_names = [m[0] for m in metric_objects]
    data = {m: [] for m in metric_names}
    raw_data = []
    all_measurements = MetricRecord.objects.filter(metric__daily=True)

    for m in all_measurements:
        data[m.metric.name].append(m.measurement)

    # Get the longest array so we can pad data
    longest_array = 0

    for metric_name, measurements in data.items():
        if len(measurements) > longest_array:
            longest_array = len(measurements)

    for metric_name, measurements in data.items():
        # Pad left side of array with 0's where no data was entered
        data[metric_name] = [0] * (longest_array - len(data[metric_name])) + data[metric_name]
        raw_data.append(data[metric_name])

    results_raw = corrcoef(raw_data)
    metric_results = {}

    for index_1, metric_name_1,  in enumerate(data):
        for index_2, metric_name_2 in enumerate(data):
            if metric_name_1 not in metric_results:
                metric_results[metric_name_1] = []

            if metric_name_1 != metric_name_2:
                metric_results[metric_name_1].append((metric_name_1, metric_name_2, results_raw[index_1, index_2]),)

    return render(request, "correlations/correlations.html", {
                'metric_results': metric_results
            })
