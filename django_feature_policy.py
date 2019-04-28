from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__version__ = '2.1.0'

# Retrieved from Chrome document.featurePolicy.allowedFeatures()
FEATURE_NAMES = [
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
]


class FeaturePolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.get_header_value()  # to check

    def __call__(self, request):
        response = self.get_response(request)
        value = self.get_header_value()
        if value:
            response['Feature-Policy'] = value
        return response

    def get_header_value(self):
        setting = getattr(settings, 'FEATURE_POLICY', {})
        pieces = []
        for feature, values in setting.items():
            if feature not in FEATURE_NAMES:
                raise ImproperlyConfigured('Unknown feature {}'.format(feature))
            if isinstance(values, str):
                values = (values,)

            item = [feature]
            for value in values:
                if value == '*':
                    item.append("'*'")
                elif value == 'none':
                    item.append("'none'")
                elif value == 'self':
                    item.append("'self'")
                else:
                    item.append(value)
            pieces.append(' '.join(item))
        return '; '.join(pieces)
