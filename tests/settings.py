from __future__ import annotations

from typing import Any

DEBUG = False

SECRET_KEY = "not-secret"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "LOCATION": ":memory:",
    }
}

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS: list[str] = []

MIDDLEWARE = [
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "tests.testapp.urls"

STATIC_URL = "/static/"

TEMPLATES: list[dict[str, Any]] = []

USE_TZ = True
