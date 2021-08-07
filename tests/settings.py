from typing import Any, Dict, List

DEBUG = False

SECRET_KEY = "not-secret"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "LOCATION": ":memory:",
    }
}

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS: List[str] = []

MIDDLEWARE = [
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "tests.testapp.urls"

STATIC_URL = "/static/"

TEMPLATES: List[Dict[str, Any]] = []
