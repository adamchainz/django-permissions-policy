import pytest
from django.core.exceptions import ImproperlyConfigured

import django_feature_policy


def test_index(client):
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.content == b"Hello World"


def test_no_setting(client):
    resp = client.get("/")

    assert "Permissions-Policy" not in resp
    assert "Feature-Policy" not in resp


def test_empty_setting(client, settings):
    settings.PERMISSIONS_POLICY = {}
    resp = client.get("/")

    assert "Permissions-Policy" not in resp
    assert "Feature-Policy" not in resp


def test_empty_setting_old_alias(client, settings):
    settings.FEATURE_POLICY = {}
    resp = client.get("/")

    assert "Permissions-Policy" not in resp
    assert "Feature-Policy" not in resp


def test_anyone_can_geolocate(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": "*"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(*)"
    assert resp["Feature-Policy"] == "geolocation *"


def test_anyone_can_geolocate_old_alias(client, settings):
    settings.FEATURE_POLICY = {"geolocation": "*"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(*)"
    assert resp["Feature-Policy"] == "geolocation *"


def test_anyone_can_geolocate_list(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": ["*"]}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(*)"
    assert resp["Feature-Policy"] == "geolocation *"


def test_no_one_can_geolocate(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": []}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=()"
    assert resp["Feature-Policy"] == "geolocation 'none'"


def test_no_one_can_geolocate_old_none_value(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": "none"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=()"
    assert resp["Feature-Policy"] == "geolocation 'none'"


def test_self_can_geolocate(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": "self"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(self)"
    assert resp["Feature-Policy"] == "geolocation 'self'"


def test_example_com_can_geolocate(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": "https://example.com"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == 'geolocation=("https://example.com")'
    assert resp["Feature-Policy"] == "geolocation https://example.com"


def test_multiple_allowed(client, settings):
    settings.PERMISSIONS_POLICY = {"autoplay": ["self", "https://example.com"]}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == 'autoplay=(self "https://example.com")'
    assert resp["Feature-Policy"] == "autoplay 'self' https://example.com"


def test_multiple_features(client, settings):
    settings.PERMISSIONS_POLICY = {
        "accelerometer": "self",
        "geolocation": ["self", "https://example.com"],
    }

    resp = client.get("/")

    assert (
        resp["Permissions-Policy"]
        == 'accelerometer=(self), geolocation=(self "https://example.com")'
    )
    assert (
        resp["Feature-Policy"]
        == "accelerometer 'self'; geolocation 'self' https://example.com"
    )


def test_unknown_feature(client, settings):
    settings.PERMISSIONS_POLICY = {"accelerometor": "self"}

    with pytest.raises(ImproperlyConfigured):
        client.get("/")


def test_setting_changing(client, settings):
    settings.PERMISSIONS_POLICY = {}
    client.get("/")  # Forces middleware instantiation
    settings.PERMISSIONS_POLICY = {"geolocation": "self"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(self)"
    assert resp["Feature-Policy"] == "geolocation 'self'"


def test_setting_changing_old_alias(client, settings):
    settings.FEATURE_POLICY = {}
    client.get("/")  # Forces middleware instantiation
    settings.FEATURE_POLICY = {"geolocation": "self"}

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(self)"
    assert resp["Feature-Policy"] == "geolocation 'self'"


def test_other_setting_changing(client, settings):
    settings.PERMISSIONS_POLICY = {"geolocation": "self"}
    client.get("/")  # Forces middleware instantiation
    settings.SECRET_KEY = "foobar"

    resp = client.get("/")

    assert resp["Permissions-Policy"] == "geolocation=(self)"
    assert resp["Feature-Policy"] == "geolocation 'self'"


def test_middleware_alias():
    assert (
        django_feature_policy.FeaturePolicyMiddleware
        is django_feature_policy.PermissionsPolicyMiddleware
    )
