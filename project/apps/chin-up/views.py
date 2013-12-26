from django.shortcuts import render


def home(request):
    return render(request, 'chin-up/home.html', locals())
