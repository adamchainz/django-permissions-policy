from __future__ import annotations

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.http.response import HttpResponseBase
from django.test import override_settings
from django.test import RequestFactory
from django.test import SimpleTestCase

from django_permissions_policy import PermissionsPolicyMiddleware


class PermissionsPolicyMiddlewareTests(SimpleTestCase):
    request_factory = RequestFactory()

    def test_index(self):
        resp = self.client.get("/")

        assert resp.status_code == 200
        assert resp.content == b"Hello World"

    def test_no_setting(self):
        resp = self.client.get("/")

        # django-stubs missing method
        # https://github.com/typeddjango/django-stubs/pull/1099
        assert "Permissions-Policy" not in resp  # type: ignore [operator]

    def test_empty_setting(self):
        with override_settings(PERMISSIONS_POLICY={}):
            resp = self.client.get("/")

        # django-stubs missing method
        # https://github.com/typeddjango/django-stubs/pull/1099
        assert "Permissions-Policy" not in resp  # type: ignore [operator]

    def test_anyone_can_geolocate_list(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": ["*"]}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(*)"

    def test_no_one_can_geolocate(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": []}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=()"

    def test_no_one_can_geolocate_old_none_value(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": "none"}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=()"

    def test_self_can_geolocate(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(self)"

    def test_example_com_can_geolocate(self):
        with override_settings(
            PERMISSIONS_POLICY={"geolocation": "https://example.com"}
        ):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == 'geolocation=("https://example.com")'

    def test_multiple_allowed(self):
        with override_settings(
            PERMISSIONS_POLICY={"autoplay": ["self", "https://example.com"]}
        ):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == 'autoplay=(self "https://example.com")'

    def test_multiple_features(self):
        with override_settings(
            PERMISSIONS_POLICY={
                "accelerometer": "self",
                "geolocation": ["self", "https://example.com"],
            }
        ):
            resp = self.client.get("/")

        assert (
            resp["Permissions-Policy"]
            == 'accelerometer=(self), geolocation=(self "https://example.com")'
        )

    def test_unknown_feature(self):
        with override_settings(PERMISSIONS_POLICY={"accelerometor": "self"}):
            with pytest.raises(ImproperlyConfigured):
                self.client.get("/")

    def test_setting_changing(self):
        with override_settings(PERMISSIONS_POLICY={}):
            self.client.get("/")  # Forces middleware instantiation

        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(self)"

    def test_other_setting_changing(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            self.client.get("/")  # Forces middleware instantiation

            with override_settings(SECRET_KEY="foobar"):
                resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(self)"

    async def test_async(self):
        async def dummy_async_view(request):
            return HttpResponse("Hello!")

        middleware = PermissionsPolicyMiddleware(dummy_async_view)
        request = self.request_factory.get("/", HTTP_HX_REQUEST="true")

        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            result = middleware(request)
            assert not isinstance(result, HttpResponseBase)  # type narrow
            response = await result

        assert response["Permissions-Policy"] == "geolocation=(self)"
