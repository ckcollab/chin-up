from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'stats[/]$', 'stats.views.stats_view', name='stats'),
)
