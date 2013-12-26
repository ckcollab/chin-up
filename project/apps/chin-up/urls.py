from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'chin-up.views.home', name='home'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # static files (images, css, javascript, etc.)
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
