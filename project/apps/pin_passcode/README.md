django settings:
 - PIN_PASSCODE_USERNAME = 'eric' #user to sign in as, defaults to "admin"
 - PIN_PASSCODE_PIN = 1234 #pass to login with

add to urls.py:
 - url(r'^admin/', include(admin.site.urls)),

add to settings file:
 - installed apps ++
 - middleware ++
