from __future__ import annotations

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings

from django_permissions_policy.decorators import (
    permissions_policy_override,
    permissions_policy_report_only_override,
)


class PermissionsPolicyOverrideTests(SimpleTestCase):
    def test_override_sets_header(self):
        resp = self.client.get("/override/")

        assert resp["Permissions-Policy"] == "geolocation=()"

    def test_override_replaces_global_setting(self):
        with override_settings(PERMISSIONS_POLICY={"autoplay": []}):
            resp = self.client.get("/override/")

        assert resp["Permissions-Policy"] == "geolocation=()"

    def test_override_empty_disables_header(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": []}):
            resp = self.client.get("/override-disabled/")

        assert "Permissions-Policy" not in resp

    def test_override_does_not_affect_report_only(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": []}):
            resp = self.client.get("/override/")

        assert resp["Permissions-Policy-Report-Only"] == "autoplay=()"

    def test_override_invalid_config_raises(self):
        with pytest.raises(ImproperlyConfigured):
            permissions_policy_override({"unknown-feature": []})

    async def test_async_override_sets_header(self):
        resp = await self.async_client.get("/async/override/")

        assert resp["Permissions-Policy"] == "geolocation=()"

    async def test_async_override_empty_disables_header(self):
        with override_settings(PERMISSIONS_POLICY={"geolocation": []}):
            resp = await self.async_client.get("/async/override-disabled/")

        assert "Permissions-Policy" not in resp


class PermissionsPolicyReportOnlyOverrideTests(SimpleTestCase):
    def test_report_only_override_sets_header(self):
        resp = self.client.get("/report-only-override/")

        assert resp["Permissions-Policy-Report-Only"] == "geolocation=()"

    def test_report_only_override_replaces_global_setting(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"autoplay": []}):
            resp = self.client.get("/report-only-override/")

        assert resp["Permissions-Policy-Report-Only"] == "geolocation=()"

    def test_report_only_override_empty_disables_header(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": []}):
            resp = self.client.get("/report-only-override-disabled/")

        assert "Permissions-Policy-Report-Only" not in resp

    def test_report_only_override_does_not_affect_enforced(self):
        with override_settings(PERMISSIONS_POLICY={"autoplay": []}):
            resp = self.client.get("/report-only-override/")

        assert resp["Permissions-Policy"] == "autoplay=()"

    def test_report_only_override_invalid_config_raises(self):
        with pytest.raises(ImproperlyConfigured):
            permissions_policy_report_only_override({"unknown-feature": []})

    async def test_async_report_only_override_sets_header(self):
        resp = await self.async_client.get("/async/report-only-override/")

        assert resp["Permissions-Policy-Report-Only"] == "geolocation=()"

    async def test_async_report_only_override_empty_disables_header(self):
        with override_settings(PERMISSIONS_POLICY_REPORT_ONLY={"geolocation": []}):
            resp = await self.async_client.get("/async/report-only-override-disabled/")

        assert "Permissions-Policy-Report-Only" not in resp
