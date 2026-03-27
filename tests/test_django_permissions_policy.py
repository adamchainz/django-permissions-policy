from __future__ import annotations

from http import HTTPStatus

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase, override_settings


class PermissionsPolicyMiddlewareTests(SimpleTestCase):
    request_factory = RequestFactory()

    def test_index(self):
        resp = self.client.get("/")

        assert resp.status_code == HTTPStatus.OK
        assert resp.content == b"Hello World"

    def test_no_settings(self):
        resp = self.client.get("/")

        assert "Permissions-Policy" not in resp

    def test_empty_setting(self):
        with override_settings(PERMISSIONS_POLICY={}):
            resp = self.client.get("/")

        assert "Permissions-Policy" not in resp

    def test_empty_report_only_setting(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={}):
            resp = self.client.get("/")

        assert "Permissions-Policy-Report-Only" not in resp

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
        with (
            override_settings(PERMISSIONS_POLICY={"accelerometor": "self"}),
            pytest.raises(ImproperlyConfigured),
        ):
            self.client.get("/")

    def test_setting_changing(self):
        with override_settings(PERMISSIONS_POLICY={}):
            self.client.get("/")  # Forces middleware instantiation

        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(self)"

    def test_report_only_setting_changing(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={}):
            self.client.get("/")  # Forces middleware instantiation

        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": "self"}):
            resp = self.client.get("/")

        assert resp["Permissions-Policy-Report-Only"] == "geolocation=(self)"

    def test_other_setting_changing(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            self.client.get("/")  # Forces middleware instantiation

            with override_settings(SECRET_KEY="foobar"):
                resp = self.client.get("/")

        assert resp["Permissions-Policy"] == "geolocation=(self)"

    async def test_async_no_settings(self):
        resp = await self.async_client.get("/async/")

        assert resp.status_code == HTTPStatus.OK
        assert "Permissions-Policy" not in resp
        assert "Permissions-Policy-Report-Only" not in resp

    async def test_async(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            resp = await self.async_client.get("/async/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["Permissions-Policy"] == "geolocation=(self)"

    async def test_async_report_only(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": "self"}):
            resp = await self.async_client.get("/async/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["Permissions-Policy-Report-Only"] == "geolocation=(self)"
