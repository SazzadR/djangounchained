from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve, reverse, Resolver404


def default(request):
    try:
        resolve(reverse('accounts:login'))
        has_auth = True
    except:
        has_auth = False

    return render(request, 'djangounchained/default.html', {'has_auth': has_auth})
