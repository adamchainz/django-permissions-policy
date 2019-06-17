from testapp.views import index

try:
    from django.urls import path

    urlpatterns = [path("", index, name="index")]
except ImportError:  # Django < 2.0
    from django.conf.urls import url

    urlpatterns = [url(r"^$", index, name="index")]
