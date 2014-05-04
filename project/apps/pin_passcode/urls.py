from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'pin/$', 'pin_passcode.views.form', name='pin_form'),
    url(r'pin/auth$', 'pin_passcode.views.auth', name='pin_auth'),
)
