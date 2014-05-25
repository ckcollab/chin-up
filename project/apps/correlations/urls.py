from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'correlations[/]$', 'correlations.views.correlation_view', name='correlations'),
)
