from __future__ import annotations

from collections.abc import Awaitable
from http import HTTPStatus

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseBase
from django.test import RequestFactory, SimpleTestCase, override_settings

from django_permissions_policy import PermissionsPolicyMiddleware


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
            pytest.raises(
                ImproperlyConfigured,
                match="Unknown feature 'accelerometor' in PERMISSIONS_POLICY",
            ),
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


class PermissionsPolicyMiddlewareArgumentTests(SimpleTestCase):
    request_factory = RequestFactory()

    def get_response(self, request):
        return HttpResponse("Hello World")

    async def aget_response(self, request):
        return HttpResponse("Hello World")

    @override_settings(PERMISSIONS_POLICY={"geolocation": []})
    def test_policy_argument_used_instead_of_setting(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response, policy={"geolocation": "self"}
        )

        resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy"] == "geolocation=(self)"

    @override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": []})
    def test_report_only_policy_argument_used_instead_of_setting(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response, report_only_policy={"geolocation": "self"}
        )

        resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy-Report-Only"] == "geolocation=(self)"

    @override_settings(PERMISSIONS_POLICY={"geolocation": []})
    def test_empty_policy_argument_sends_no_header(self):
        middleware = PermissionsPolicyMiddleware(self.get_response, policy={})

        resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert "Permissions-Policy" not in resp

    @override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": []})
    def test_empty_report_only_policy_argument_sends_no_header(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response, report_only_policy={}
        )

        resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert "Permissions-Policy-Report-Only" not in resp

    @override_settings(
        PERMISSIONS_POLICY={"geolocation": []},
        PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": []},
    )
    def test_none_falls_back_to_settings(self):
        middleware = PermissionsPolicyMiddleware(self.get_response)

        resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy"] == "geolocation=()"
        assert resp["Permissions-Policy-Report-Only"] == "autoplay=()"

    def test_invalid_policy_argument(self):
        with pytest.raises(
            ImproperlyConfigured,
            match="Unknown feature 'accelerometor' in 'policy' argument",
        ):
            PermissionsPolicyMiddleware(
                self.get_response, policy={"accelerometor": "self"}
            )

    def test_invalid_report_only_policy_argument(self):
        with pytest.raises(
            ImproperlyConfigured,
            match="Unknown feature 'accelerometor' in 'report_only_policy' argument",
        ):
            PermissionsPolicyMiddleware(
                self.get_response, report_only_policy={"accelerometor": "self"}
            )

    def test_invalid_setting_names_setting(self):
        with (
            override_settings(PERMISSIONS_POLICY={"accelerometor": "self"}),
            pytest.raises(
                ImproperlyConfigured,
                match="Unknown feature 'accelerometor' in PERMISSIONS_POLICY",
            ),
        ):
            PermissionsPolicyMiddleware(self.get_response)

    def test_invalid_report_only_setting_names_setting(self):
        with (
            override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"accelerometor": "self"}),
            pytest.raises(
                ImproperlyConfigured,
                match=(
                    "Unknown feature 'accelerometor' in PERMISSIONS_POLICY_REPORT_ONLY"
                ),
            ),
        ):
            PermissionsPolicyMiddleware(self.get_response)

    def test_override_settings_affects_setting_sourced_instance(self):
        middleware = PermissionsPolicyMiddleware(self.get_response)

        with override_settings(
            PERMISSIONS_POLICY={"geolocation": "self"},
            PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": "self"},
        ):
            resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy"] == "geolocation=(self)"
        assert resp["Permissions-Policy-Report-Only"] == "autoplay=(self)"

    def test_override_settings_does_not_affect_argument_sourced_instance(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response,
            policy={"geolocation": []},
            report_only_policy={"autoplay": []},
        )

        with override_settings(
            PERMISSIONS_POLICY={"geolocation": "self"},
            PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": "self"},
        ):
            resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy"] == "geolocation=()"
        assert resp["Permissions-Policy-Report-Only"] == "autoplay=()"

    def test_override_settings_does_not_affect_policy_argument_only(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response, policy={"geolocation": []}
        )

        with override_settings(PERMISSIONS_POLICY={"geolocation": "self"}):
            resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy"] == "geolocation=()"

    def test_override_settings_does_not_affect_report_only_policy_argument_only(self):
        middleware = PermissionsPolicyMiddleware(
            self.get_response, report_only_policy={"autoplay": []}
        )

        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": "self"}):
            resp = middleware(self.request_factory.get("/"))

        assert isinstance(resp, HttpResponseBase)
        assert resp["Permissions-Policy-Report-Only"] == "autoplay=()"

    @override_settings(PERMISSIONS_POLICY={"geolocation": []})
    async def test_async_policy_argument(self):
        middleware = PermissionsPolicyMiddleware(
            self.aget_response,
            policy={"geolocation": "self"},
            report_only_policy={"autoplay": "self"},
        )

        coroutine = middleware(self.request_factory.get("/"))
        assert isinstance(coroutine, Awaitable)
        resp = await coroutine
        assert isinstance(resp, HttpResponseBase)

        assert resp["Permissions-Policy"] == "geolocation=(self)"
        assert resp["Permissions-Policy-Report-Only"] == "autoplay=(self)"
