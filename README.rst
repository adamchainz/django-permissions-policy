django-feature-policy
=====================

.. image:: https://github.com/adamchainz/django-feature-policy/workflows/CI/badge.svg?branch=master
   :target: https://github.com/adamchainz/django-feature-policy/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/django-feature-policy.svg
   :target: https://pypi.python.org/pypi/django-feature-policy

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black

Set the draft security HTTP header ``Feature-Policy`` on your Django app.

Requirements
------------

Python 3.5 to 3.8 supported.

Django 2.0 to 3.0 supported.

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
      'django_feature_policy.FeaturePolicyMiddleware',
      ...
    ]

By default no header will be set, configure the setting as below.

Setting
-------

Change the ``FEATURE_POLICY`` setting to configure what ``Feature-Policy``
header gets set.

This should be a dictionary laid out with:

* Keys as the names of browser features - a full list is available on the
  `W3 Spec repository`_. The `MDN article`_ is also worth reading.
* Values as lists of strings, where each string is either an origin, e.g.
  ``'https://example.com'``, or of the special values ``'self'``, ``'none'``,
  or ``'*'``. If there is just one value, no containing list is necessary. Note
  that in the header, special values like ``'none'`` include single quotes
  around them - do not include these quotes in your Python string, they will be
  added by the middleware.

.. _W3 Spec repository: https://github.com/w3c/webappsec-feature-policy/blob/master/features.md
.. _MDN article: https://developer.mozilla.org/en-US/docs/Web/HTTP/Feature_Policy#Browser_compatibility

If the keys or values are invalid, ``ImproperlyConfigured`` will be raised at
instantiation time, or when processing a response. The current feature list is
pulled from the JavaScript API with
``document.featurePolicy.allowedFeatures()`` on Chrome.

Examples
~~~~~~~~

Disable geolocation from running in the current page and any iframe:

.. code-block:: python

    FEATURE_POLICY = {
        'geolocation': 'none',
    }

Allow autoplay from the current origin and iframes from
``https://archive.org``:

.. code-block:: python

    FEATURE_POLICY = {
        'autoplay': ['self', 'https://archive.org'],
    }
