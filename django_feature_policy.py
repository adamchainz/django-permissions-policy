from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import cached_property

# Retrieved from Chrome document.featurePolicy.allowedFeatures()
# with flag "Experimental Web Platform features" turned on
FEATURE_NAMES = {
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
    "ch-ua-model",
    "ch-ua-platform",
    "ch-viewport-width",
    "ch-width",
    "document-domain",
    "document-write",
    "downloads-without-user-activation",
    "encrypted-media",
    "execution-while-not-rendered",
    "execution-while-out-of-viewport",
    "focus-without-user-activation",
    "font-display-late-swap",
    "forms",
    "fullscreen",
    "geolocation",
    "gyroscope",
    "hid",
    "idle-detection",
    "layout-animations",
    "lazyload",
    "loading-frame-default-eager",
    "magnetometer",
    "microphone",
    "midi",
    "modals",
    "orientation-lock",
    "oversized-images",
    "payment",
    "picture-in-picture",
    "pointer-lock",
    "popups",
    "presentation",
    "scripts",
    "serial",
    "speaker",
    "sync-script",
    "sync-xhr",
    "top-navigation",
    "unoptimized-lossless-images",
    "unoptimized-lossless-images-strict",
    "unoptimized-lossy-images",
    "unsized-media",
    "usb",
    "vertical-scroll",
    "vr",
    "wake-lock",
}


class FeaturePolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.header_value  # Access at setup so ImproperlyConfigured can be raised
        receiver(setting_changed)(self.clear_header_value)

    def __call__(self, request):
        response = self.get_response(request)
        value = self.header_value
        if value:
            response["Feature-Policy"] = value
        return response

    @cached_property
    def header_value(self):
        setting = getattr(settings, "FEATURE_POLICY", {})
        pieces = []
        for feature, values in sorted(setting.items()):
            if feature not in FEATURE_NAMES:
                raise ImproperlyConfigured("Unknown feature {}".format(feature))
            if isinstance(values, str):
                values = (values,)

            item = [feature]
            for value in values:
                if value == "none":
                    item.append("'none'")
                elif value == "self":
                    item.append("'self'")
                else:
                    item.append(value)
            pieces.append(" ".join(item))
        return "; ".join(pieces)

    def clear_header_value(self, setting, **kwargs):
        if setting == "FEATURE_POLICY":
            try:
                del self.header_value
            except AttributeError:
                pass
