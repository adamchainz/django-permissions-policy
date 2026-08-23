from __future__ import annotations

from collections.abc import Awaitable, Callable

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property

_FEATURE_NAMES: set[str] = {
    # Chrome features
    # https://github.com/chromium/chromium/raw/refs/heads/main/services/network/public/cpp/permissions_policy/permissions_policy_features.json5
    "accelerometer",
    "ambient-light-sensor",
    "aria-notify",
    "autofill",
    "autoplay",
    "bluetooth",
    "browsing-topics",
    "camera",
    "captured-surface-control",
    "ch-device-memory",
    "ch-downlink",
    "ch-dpr",
    "ch-ect",
    "ch-prefers-color-scheme",
    "ch-prefers-reduced-motion",
    "ch-prefers-reduced-transparency",
    "ch-rtt",
    "ch-save-data",
    "ch-ua",
    "ch-ua-arch",
    "ch-ua-bitness",
    "ch-ua-form-factors",
    "ch-ua-full-version",
    "ch-ua-full-version-list",
    "ch-ua-high-entropy-values",
    "ch-ua-mobile",
    "ch-ua-model",
    "ch-ua-platform",
    "ch-ua-platform-version",
    "ch-ua-wow64",
    "ch-viewport-height",
    "ch-viewport-width",
    "ch-width",
    "clipboard-read",
    "clipboard-write",
    "compute-pressure",
    "cross-origin-isolated",
    "deferred-fetch",
    "deferred-fetch-minimal",
    "device-attributes",
    "digital-credentials-create",
    "digital-credentials-get",
    "display-capture",
    "encrypted-media",
    "execution-while-not-rendered",
    "execution-while-out-of-viewport",
    "focus-without-user-activation",
    "fullscreen",
    "gamepad",
    "geolocation",
    "gyroscope",
    "hid",
    "identity-credentials-get",
    "idle-detection",
    "interest-cohort",
    "keyboard-map",
    "language-detector",
    "language-model",
    "local-fonts",
    "local-network",
    "local-network-access",
    "loopback-network",
    "magnetometer",
    "manual-text",
    "media-playback-while-not-visible",
    "microphone",
    "midi",
    "on-device-speech-recognition",
    "otp-credentials",
    "payment",
    "picture-in-picture",
    "private-state-token-issuance",
    "private-state-token-redemption",
    "publickey-credentials-create",
    "publickey-credentials-get",
    "rewriter",
    "screen-wake-lock",
    "serial",
    "shared-storage",
    "shared-storage-select-url",
    "speaker-selection",
    "storage-access",
    "summarizer",
    "sync-xhr",
    "tools",
    "translator",
    "unload",
    "usb",
    "vertical-scroll",
    "web-app-installation",
    "web-share",
    "webnn",
    "window-management",
    "writer",
    "xr-spatial-tracking",
    # Firefox-only features
    # https://github.com/mozilla/gecko-dev/raw/refs/heads/master/dom/security/featurepolicy/FeaturePolicyUtils.cpp
    "document-domain",
    "vr",
}


class PermissionsPolicyMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
        *,
        policy: dict[str, str | list[str] | tuple[str]] | None = None,
        report_only_policy: dict[str, str | list[str] | tuple[str]] | None = None,
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            markcoroutinefunction(self)

        # Values from arguments can never change, so compute eagerly. This also
        # validates them, like the eager access of the setting-based values below.
        if policy is not None:
            self.permissions_policy = self.compute_header_value(
                policy, name="'policy' argument"
            )
        else:
            self.permissions_policy  # noqa: B018 - Access at setup so ImproperlyConfigured can be raised

        if report_only_policy is not None:
            self.permissions_policy_report_only = self.compute_header_value(
                report_only_policy, name="'report_only_policy' argument"
            )
        else:
            self.permissions_policy_report_only  # noqa: B018 - Access at setup so ImproperlyConfigured can be raised

        self.policy_from_argument = policy is not None
        self.report_only_policy_from_argument = report_only_policy is not None

        if not (self.policy_from_argument and self.report_only_policy_from_argument):
            receiver(setting_changed)(self.clear_header_value)

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(request)
        response = self.get_response(request)
        assert isinstance(response, HttpResponseBase)  # type narrow
        return self._apply_headers(response)

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        result = self.get_response(request)
        assert not isinstance(result, HttpResponseBase)  # type narrow
        response = await result
        return self._apply_headers(response)

    def _apply_headers(self, response: HttpResponseBase) -> HttpResponseBase:
        if hasattr(response, "_permissions_policy_override"):
            if response._permissions_policy_override:
                response["Permissions-Policy"] = response._permissions_policy_override
        elif value := self.permissions_policy:
            response["Permissions-Policy"] = value

        if hasattr(response, "_permissions_policy_report_only_override"):
            if response._permissions_policy_report_only_override:
                response["Permissions-Policy-Report-Only"] = (
                    response._permissions_policy_report_only_override
                )
        elif value := self.permissions_policy_report_only:
            response["Permissions-Policy-Report-Only"] = value

        return response

    @cached_property
    def permissions_policy(self) -> str:
        return self.compute_header_value(
            getattr(settings, "PERMISSIONS_POLICY", {}),
            name="PERMISSIONS_POLICY",
        )

    @cached_property
    def permissions_policy_report_only(self) -> str:
        return self.compute_header_value(
            getattr(settings, "PERMISSIONS_POLICY_REPORT_ONLY", {}),
            name="PERMISSIONS_POLICY_REPORT_ONLY",
        )

    @staticmethod
    def compute_header_value(
        policy: dict[str, str | list[str] | tuple[str]],
        name: str,
    ) -> str:
        pieces = []
        for feature, values in sorted(policy.items()):
            if feature not in _FEATURE_NAMES:
                raise ImproperlyConfigured(f"Unknown feature '{feature}' in {name}")
            if isinstance(values, str):
                values = (values,)

            item = []
            for value in values:
                if value == "none":
                    # 'none' was previously supported as a special token for
                    # Feature-Policy, now can be represented by the empty list.
                    pass
                elif value in ("self", "*"):
                    item.append(value)
                else:
                    item.append(f'"{value}"')  # noqa: B028
            pieces.append(feature + "=(" + " ".join(item) + ")")
        return ", ".join(pieces)

    def clear_header_value(self, setting: str, **kwargs: object) -> None:
        if setting == "PERMISSIONS_POLICY":
            if self.policy_from_argument:
                return
            try:
                del self.permissions_policy
            except AttributeError:
                pass
        elif setting == "PERMISSIONS_POLICY_REPORT_ONLY":
            if self.report_only_policy_from_argument:
                return
            try:
                del self.permissions_policy_report_only
            except AttributeError:
                pass
