from importlib import import_module

from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, HttpResponse, HttpResponseRedirect


def form(request):
    return render(request, 'pin_passcode/form.html')


def auth(request):
    if request.method == 'POST':
        pin = request.POST.get('pin', None)
        if pin == settings.PIN_PASSCODE_PIN:
            user = get_user_model().objects.get(username=settings.PIN_PASSCODE_USERNAME)
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            #if not hasattr(request.user, 'session'):
            #    engine = import_module(settings.SESSION_ENGINE)
            #    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
            #    request.META = {}
            #    request.user.session = engine.SessionStore(session_key)

            #user = authenticate(username=settings.PIN_PASSCODE_USERNAME, password='eric')
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', '/'))
    # if request pin is right, login as settings.PIN_PASSCODE_USERNAME
    #print request

    return HttpResponse(status=401)
