DEBUG = False

SECRET_KEY = 'not-secret'

DATABASES = {}

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = []

MIDDLEWARE = [
    'django_feature_policy.FeaturePolicyMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'tests.testapp.urls'

STATIC_URL = '/static/'

TEMPLATES = []
