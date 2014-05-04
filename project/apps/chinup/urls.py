from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('auth', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', 'chinup.views.home', name='home'),
    url(r'^input[/]$', 'chinup.views.input', name='input'),
    url(r'^', include('pin_passcode.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # static files (images, css, javascript, etc.)
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
