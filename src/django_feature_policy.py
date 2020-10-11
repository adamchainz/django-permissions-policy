from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import cached_property

FEATURE_NAMES = {
    # Base and Chrome-only features
    # Retrieved from Chrome document.featurePolicy.allowedFeatures()
    # with flag "Experimental Web Platform features" turned on:
    "accelerometer",
    "ambient-light-sensor",
    "autoplay",
    "camera",
    "ch-device-memory",
    "ch-downlink",
    "ch-dpr",
    "ch-ect",
    "ch-lang",
    "ch-rtt",
    "ch-ua",
    "ch-ua-arch",
    "ch-ua-full-version",
    "ch-ua-mobile",
    "ch-ua-model",
    "ch-ua-platform",
    "ch-ua-platform-version",
    "ch-viewport-width",
    "ch-width",
    "clipboard-read",
    "clipboard-write",
    "cross-origin-isolated",
    "document-domain",
    "document-write",
    "downloads",
    "encrypted-media",
    "execution-while-not-rendered",
    "execution-while-out-of-viewport",
    "focus-without-user-activation",
    "forms",
    "fullscreen",
    "gamepad",
    "geolocation",
    "gyroscope",
    "hid",
    "idle-detection",
    "magnetometer",
    "microphone",
    "midi",
    "modals",
    "orientation-lock",
    "payment",
    "picture-in-picture",
    "pointer-lock",
    "popups",
    "presentation",
    "publickey-credentials-get",
    "screen-wake-lock",
    "scripts",
    "serial",
    "sync-script",
    "sync-xhr",
    "top-navigation",
    "usb",
    "vertical-scroll",
    "xr-spatial-tracking",
    # Firefox-only features.
    # Retrieved from Firefox document.featurePolicy.allowedFeatures()
    # with dom.security.featurePolicy.header.enabled preference set to true
    # in about:config (plus a restart):
    "display-capture",
    "speaker",
    "vr",
    "web-share",
}


class PermissionsPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.header_value  # Access at setup so ImproperlyConfigured can be raised
        receiver(setting_changed)(self.clear_header_value)

    def __call__(self, request):
        response = self.get_response(request)
        value = self.header_value
        if value:
            response["Permissions-Policy"] = value
            response["Feature-Policy"] = self.old_header_value
        return response

    @cached_property
    def header_value(self):
        setting = self.get_setting()
        pieces = []
        for feature, values in sorted(setting.items()):
            if feature not in FEATURE_NAMES:
                raise ImproperlyConfigured("Unknown feature {}".format(feature))
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
                    item.append('"{}"'.format(value))
            pieces.append(feature + "=(" + " ".join(item) + ")")
        return ", ".join(pieces)

    @cached_property
    def old_header_value(self):
        setting = self.get_setting()
        pieces = []
        for feature, values in sorted(setting.items()):
            if isinstance(values, str):
                values = (values,)

            item = [feature]
            if not values:
                item.append("'none'")
            else:
                for value in values:
                    if value == "none":
                        item.append("'none'")
                    elif value == "self":
                        item.append("'self'")
                    else:
                        item.append(value)
            pieces.append(" ".join(item))
        return "; ".join(pieces)

    def get_setting(self):
        setting = getattr(settings, "PERMISSIONS_POLICY", None)
        if not setting:
            setting = getattr(settings, "FEATURE_POLICY", {})
        return setting

    def clear_header_value(self, setting, **kwargs):
        if setting in ("PERMISSIONS_POLICY", "FEATURE_POLICY"):
            try:
                del self.header_value
            except AttributeError:
                pass


FeaturePolicyMiddleware = PermissionsPolicyMiddleware
