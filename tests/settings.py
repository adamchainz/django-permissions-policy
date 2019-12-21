DEBUG = False

SECRET_KEY = "not-secret"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "LOCATION": ":memory:"}
}

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = []

MIDDLEWARE = [
    "django_feature_policy.FeaturePolicyMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "tests.testapp.urls"

STATIC_URL = "/static/"

TEMPLATES = []
