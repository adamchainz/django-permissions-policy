from __future__ import annotations

from django.urls import path

from tests.testapp import views

urlpatterns = [
    path("", views.index),
    path("async/", views.async_index),
    path("override/", views.override_index),
    path("override-disabled/", views.override_disabled_index),
    path("report-only-override/", views.report_only_override_index),
    path("report-only-override-disabled/", views.report_only_override_disabled_index),
    path("async/override/", views.async_override_index),
    path("async/override-disabled/", views.async_override_disabled_index),
    path("async/report-only-override/", views.async_report_only_override_index),
    path(
        "async/report-only-override-disabled/",
        views.async_report_only_override_disabled_index,
    ),
]
