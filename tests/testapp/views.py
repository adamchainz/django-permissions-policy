from __future__ import annotations

from django.http import HttpResponse

from django_permissions_policy.decorators import (
    permissions_policy_override,
    permissions_policy_report_only_override,
)


def index(request):
    return HttpResponse("Hello World")


async def async_index(request):
    return HttpResponse("Hello World")


@permissions_policy_override({"geolocation": []})
def override_index(request):
    return HttpResponse("Hello World")


@permissions_policy_override({})
def override_disabled_index(request):
    return HttpResponse("Hello World")


@permissions_policy_report_only_override({"geolocation": []})
def report_only_override_index(request):
    return HttpResponse("Hello World")


@permissions_policy_report_only_override({})
def report_only_override_disabled_index(request):
    return HttpResponse("Hello World")


@permissions_policy_override({"geolocation": []})
async def async_override_index(request):
    return HttpResponse("Hello World")


@permissions_policy_override({})
async def async_override_disabled_index(request):
    return HttpResponse("Hello World")


@permissions_policy_report_only_override({"geolocation": []})
async def async_report_only_override_index(request):
    return HttpResponse("Hello World")


@permissions_policy_report_only_override({})
async def async_report_only_override_disabled_index(request):
    return HttpResponse("Hello World")
