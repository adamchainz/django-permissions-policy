=========================
django-permissions-policy
=========================

.. image:: https://img.shields.io/github/workflow/status/adamchainz/django-permissions-policy/CI/main?style=for-the-badge
   :target: https://github.com/adamchainz/django-permissions-policy/actions?workflow=CI

.. image:: https://img.shields.io/codecov/c/github/adamchainz/django-permissions-policy/main?style=for-the-badge
   :target: https://app.codecov.io/gh/adamchainz/django-permissions-policy

.. image:: https://img.shields.io/pypi/v/django-permissions-policy.svg?style=for-the-badge
   :target: https://pypi.org/project/django-permissions-policy/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

Set the draft security HTTP header ``Permissions-Policy`` (previously ``Feature-Policy``) on your Django app.

Requirements
------------

Python 3.6 to 3.9 supported.

Django 2.2 to 3.2 supported.

----

**Are your tests slow?**
Check out my book `Speed Up Your Django Tests <https://gumroad.com/l/suydt>`__ which covers loads of best practices so you can write faster, more accurate tests.

----

Installation
------------

1. Install with **pip**:

.. code-block:: sh

    python -m pip install django-permissions-policy

2. Add the middleware in your ``MIDDLEWARE`` setting. It’s best to add it
after Django's ``SecurityMiddleware``, so it adds the header at the same point
in your stack:

.. code-block:: python

    MIDDLEWARE = [
        ...,
        "django.middleware.security.SecurityMiddleware",
        "django_permissions_policy.PermissionsPolicyMiddleware",
        ...,
    ]

3. Add the ``PERMISSIONS_POLICY`` setting to your settings, naming at least one
   feature. Here’s an example that sets a strict policy to disable many
   potentially privacy-invading and annoying features for all scripts:

   .. code-block:: python

       PERMISSIONS_POLICY = {
           "accelerometer": [],
           "ambient-light-sensor": [],
           "autoplay": [],
           "camera": [],
           "display-capture": [],
           "document-domain": [],
           "encrypted-media": [],
           "fullscreen": [],
           "geolocation": [],
           "gyroscope": [],
           "interest-cohort": [],
           "magnetometer": [],
           "microphone": [],
           "midi": [],
           "payment": [],
           "usb": [],
       }

   See below for more information on the setting.

Setting
-------

Change the ``PERMISSIONS_POLICY`` setting to configure the contents of the
header.

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

For backwards compatibility with old configuration, the value ``'none'`` is
supported in lists, but ignored - it's preferable to use the empty list
instead. It doesn't make sense to specify ``'none'`` alongside other values.

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
