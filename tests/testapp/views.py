from __future__ import annotations

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")
