from __future__ import annotations

from collections.abc import Awaitable
from typing import Callable

from asgiref.sync import iscoroutinefunction
from asgiref.sync import markcoroutinefunction
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property

_FEATURE_NAMES: set[str] = {
    # Base and Chrome-only features
    # Retrieved from Chrome document.featurePolicy.allowedFeatures()
    # with flag "Experimental Web Platform features" turned on:
    "accelerometer",
    "ambient-light-sensor",
    "attribution-reporting",
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
    "join-ad-interest-group",
    "keyboard-map",
    "local-fonts",
    "magnetometer",
    "microphone",
    "midi",
    "otp-credentials",
    "payment",
    "picture-in-picture",
    "popins",
    "private-aggregation",
    "private-state-token-issuance",
    "private-state-token-redemption",
    "publickey-credentials-create",
    "publickey-credentials-get",
    "run-ad-auction",
    "screen-wake-lock",
    "serial",
    "shared-storage",
    "shared-storage-select-url",
    "speaker-selection",
    "storage-access",
    "sync-xhr",
    "unload",
    "usb",
    "vertical-scroll",
    "web-app-installation",
    "window-management",
    "xr-spatial-tracking",
    # Firefox-only features.
    # Retrieved from Firefox document.featurePolicy.allowedFeatures()
    # with dom.security.featurePolicy.header.enabled preference set to true
    # in about:config (plus a restart):
    "document-domain",
    "vr",
    "web-share",
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
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            markcoroutinefunction(self)

        self.header_value  # Access at setup so ImproperlyConfigured can be raised
        receiver(setting_changed)(self.clear_header_value)

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(request)
        response = self.get_response(request)
        assert isinstance(response, HttpResponseBase)  # type narrow
        value = self.header_value
        if value:
            response["Permissions-Policy"] = value
        return response

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        result = self.get_response(request)
        assert not isinstance(result, HttpResponseBase)  # type narrow
        response = await result
        value = self.header_value
        if value:  # pragma: no branch
            response["Permissions-Policy"] = value
        return response

    @cached_property
    def header_value(self) -> str:
        setting: dict[str, str | list[str] | tuple[str]] = getattr(
            settings, "PERMISSIONS_POLICY", {}
        )
        pieces = []
        for feature, values in sorted(setting.items()):
            if feature not in _FEATURE_NAMES:
                raise ImproperlyConfigured(f"Unknown feature {feature}")
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
            try:
                del self.header_value
            except AttributeError:
                pass
