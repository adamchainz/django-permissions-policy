from typing import Callable, Dict, List, Tuple, Union

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.utils.functional import cached_property

FEATURE_NAMES = {
    # Base and Chrome-only features
    # Retrieved from Chrome document.featurePolicy.allowedFeatures()
    # with flag "Experimental Web Platform features" turned on:
    "accelerometer",
    "ambient-light-sensor",
    "attribution-reporting",
    "autoplay",
    "camera",
    "ch-device-memory",
    "ch-downlink",
    "ch-dpr",
    "ch-ect",
    "ch-lang",
    "ch-prefers-color-scheme",
    "ch-rtt",
    "ch-ua",
    "ch-ua-arch",
    "ch-ua-bitness",
    "ch-ua-full-version",
    "ch-ua-mobile",
    "ch-ua-model",
    "ch-ua-platform",
    "ch-ua-platform-version",
    "ch-ua-reduced",
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
    "interest-cohort",
    "magnetometer",
    "microphone",
    "midi",
    "otp-credentials",
    "payment",
    "picture-in-picture",
    "publickey-credentials-get",
    "screen-wake-lock",
    "serial",
    "shared-autofill",
    "sync-xhr",
    "usb",
    "vertical-scroll",
    "window-placement",
    "xr-spatial-tracking",
    # Firefox-only features.
    # Retrieved from Firefox document.featurePolicy.allowedFeatures()
    # with dom.security.featurePolicy.header.enabled preference set to true
    # in about:config (plus a restart):
    "speaker",
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
        setting: Dict[str, Union[str, List[str], Tuple[str]]] = getattr(
            settings, "PERMISSIONS_POLICY", {}
        )
        pieces = []
        for feature, values in sorted(setting.items()):
            if feature not in FEATURE_NAMES:
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
