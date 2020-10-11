django-feature-policy
=====================

.. image:: https://github.com/adamchainz/django-feature-policy/workflows/CI/badge.svg?branch=master
   :target: https://github.com/adamchainz/django-feature-policy/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/django-feature-policy.svg
   :target: https://pypi.org/project/django-feature-policy/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black

Set the draft security HTTP header ``Permissions-Policy`` (previously ``Feature-Policy``) on your Django app.

Requirements
------------

Python 3.5 to 3.8 supported.

Django 2.2 to 3.1 supported.

----

**Are your tests slow?**
Check out my book `Speed Up Your Django Tests <https://gumroad.com/l/suydt>`__ which covers loads of best practices so you can write faster, more accurate tests.

----

Installation
------------

Install with **pip**:

.. code-block:: sh

    python -m pip install django-feature-policy

Then add the middleware, best after Django's ``SecurityMiddleware`` as it does
similar addition of security headers that you'll want on every response:

.. code-block:: python

    MIDDLEWARE = [
      ...
      'django.middleware.security.SecurityMiddleware',
      'django_feature_policy.PermissionsPolicyMiddleware',
      ...
    ]

The middleware will set the ``Permissions-Policy`` header, and also set it with
the previous name ``Feature-Policy``, for backwards compatibility with older
browsers.

The header will not be set until you configure the setting to set at least one
policy, as below.

(For backwards compatibility, the middleware is also importable from the alias
``FeaturePolicyMiddleware``.)

Setting
-------

Change the ``PERMISSIONS_POLICY`` setting to configure the contents of the
header.

(For backwards compatibility, the ``FEATURE_POLICY`` setting will also be read
if ``PERMISSIONS_POLICY`` is not defined.)

The setting should be a dictionary laid out with:

* Keys as the names of browser features - a full list is available on the
  `W3 Spec repository`_. The `MDN article`_ is also worth reading.
* Values as lists of strings, where each string is either an origin, e.g.
  ``'https://example.com'``, or of the special values ``'self'`` or ``'*'``. If
  there is just one value, no containing list is necessary. To represent no
  origins being allowed, use an empty list.

  Note that in the header, domains are wrapped in double quotes - do not
  include these quotes within your Python string, as they will be added by the
  middleware.

.. _W3 Spec repository: https://github.com/w3c/webappsec-permissions-policy/blob/master/features.md
.. _MDN article: https://developer.mozilla.org/en-US/docs/Web/HTTP/Feature_Policy#Browser_compatibility

If the keys or values are invalid, ``ImproperlyConfigured`` will be raised at
instantiation time, or when processing a response. The current feature list is
pulled from the JavaScript API with
``document.featurePolicy.allowedFeatures()`` on Chrome.

For backwards compatibility with the old ``Feature-Policy`` header and
configuration, the value ``'none'`` is supported in lists, but ignored - it's
preferable to use the empty list instead. It doesn't make sense to specify
``'none'`` alongside other values.

Examples
~~~~~~~~

Disable geolocation entirely, for the current origin and any iframes:

.. code-block:: python

    PERMISSIONS_POLICY = {
        "geolocation": [],
    }

Allow autoplay from only the current origin and iframes from
``https://archive.org``:

.. code-block:: python

    PERMISSIONS_POLICY = {
        "autoplay": ["self", "https://archive.org"],
    }

Allow autoplay from all origins:

.. code-block:: python

    PERMISSIONS_POLICY = {
        "autoplay": "*",
    }
