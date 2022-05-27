from __future__ import annotations

from typing import Callable

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
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
    "camera",
    "ch-device-memory",
    "ch-downlink",
    "ch-dpr",
    "ch-ect",
    "ch-partitioned-cookies",
    "ch-prefers-color-scheme",
    "ch-rtt",
    "ch-save-data",
    "ch-ua",
    "ch-ua-arch",
    "ch-ua-bitness",
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
    "cross-origin-isolated",
    "display-capture",
    "document-domain",
    "encrypted-media",
    "execution-while-not-rendered",
    "execution-while-out-of-viewport",
    "focus-without-user-activation",
    "fullscreen",
    "gamepad",
    "geolocation",
    "gyroscope",
    "hid",
    "idle-detection",
    "keyboard-map",
    "local-fonts",
    "magnetometer",
    "microphone",
    "midi",
    "otp-credentials",
    "payment",
    "picture-in-picture",
    "publickey-credentials-get",
    "screen-wake-lock",
    "serial",
    "sync-xhr",
    "usb",
    "vertical-scroll",
    "window-placement",
    "xr-spatial-tracking",
    # The 'interest-cohort' feature was removed from Chrome when FLoC was
    # removed. But the new replacement proposal, "The Topics API", says that
    # Chrome will respect this feature name to disable it:
    # https://github.com/patcg-individual-drafts/topics
    "interest-cohort",
    # Firefox-only features.
    # Retrieved from Firefox document.featurePolicy.allowedFeatures()
    # with dom.security.featurePolicy.header.enabled preference set to true
    # in about:config (plus a restart):
    "speaker-selection",
    "vr",
    "web-share",
}


class PermissionsPolicyMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.header_value  # Access at setup so ImproperlyConfigured can be raised
        receiver(setting_changed)(self.clear_header_value)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        value = self.header_value
        if value:
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
                    item.append(f'"{value}"')
            pieces.append(feature + "=(" + " ".join(item) + ")")
        return ", ".join(pieces)

    def clear_header_value(self, setting: str, **kwargs: object) -> None:
        if setting == "PERMISSIONS_POLICY":
            try:
                del self.header_value
            except AttributeError:
                pass
