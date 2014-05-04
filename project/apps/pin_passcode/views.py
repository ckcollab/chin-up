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

            login(request, user)
            return HttpResponse(status=200)

    return HttpResponse(status=401)
