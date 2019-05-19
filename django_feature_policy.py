from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import cached_property

__version__ = '2.3.0'

# Retrieved from Chrome document.featurePolicy.allowedFeatures()
FEATURE_NAMES = {
    'accelerometer',
    'ambient-light-sensor',
    'autoplay',
    'camera',
    'document-domain',
    'document-write',
    'encrypted-media',
    'font-display-late-swap',
    'fullscreen',
    'geolocation',
    'gyroscope',
    'layout-animations',
    'lazyload',
    'legacy-image-formats',
    'magnetometer',
    'microphone',
    'midi',
    'oversized-images',
    'payment',
    'picture-in-picture',
    'speaker',
    'sync-script',
    'sync-xhr',
    'unoptimized-images',
    'unsized-media',
    'usb',
    'vertical-scroll',
    'vr',
    'wake-lock',
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
            response['Feature-Policy'] = value
        return response

    @cached_property
    def header_value(self):
        setting = getattr(settings, 'FEATURE_POLICY', {})
        pieces = []
        for feature, values in sorted(setting.items()):
            if feature not in FEATURE_NAMES:
                raise ImproperlyConfigured('Unknown feature {}'.format(feature))
            if isinstance(values, str):
                values = (values,)

            item = [feature]
            for value in values:
                if value == 'none':
                    item.append("'none'")
                elif value == 'self':
                    item.append("'self'")
                else:
                    item.append(value)
            pieces.append(' '.join(item))
        return '; '.join(pieces)

    def clear_header_value(self, setting, **kwargs):
        if setting == 'FEATURE_POLICY':
            try:
                del self.header_value
            except AttributeError:
                pass
