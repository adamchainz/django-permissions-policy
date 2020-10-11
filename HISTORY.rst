History
=======

3.5.0 (2020-10-11)
------------------

* Drop Django 2.0 and 2.1 support.
* Move license from ISC to MIT License.
* Update for the rename of the header from ``Feature-Policy`` to
  ``Permissions-Policy``. This means the middleware has been renamed to
  ``PermissionsPolicyMiddleware`` and the setting has been renamed to
  ``PERMISSIONS_POLICY``. The old names are supported as aliases for backwards
  compatibility. The middleware also sets both the old and new names for
  compatibility with older browsers.
* Updated to the latest set of features from Chrome 86.

  New features:

  - ``ch-ua-platform-version``
  - ``clipboard-read``
  - ``clipboard-write``
  - ``cross-origin-isolated``
  - ``gamepad``
  - ``publickey-credentials-get``

  Removed features:

  - ``layout-animations``
  - ``lazyload``
  - ``loading-frame-default-eager``
* Added features from Firefox 81. This adds some unique features, and restores
  some features that Chrome has removed.

  New features:

  - ``display-capture``
  - ``web-share``

  Restored features:

  - ``speaker``
  - ``vr``

3.4.0 (2020-05-24)
------------------

* Updated to the latest set of features from Chrome 83.

  New features:

  - ``ch-ua-full-version``
  - ``screen-wake-lock``

  Removed features:

  - ``font-display-late-swap``
  - ``oversized-images``
  - ``unoptimized-lossless-images``
  - ``unoptimized-lossless-images-strict``
  - ``unoptimized-lossy-images``
  - ``unsized-media``
  - ``wake-lock``

* Added Django 3.1 support.

3.3.0 (2020-04-09)
------------------

* Dropped Django 1.11 support. Only Django 2.0+ is supported now.
* Updated to the latest set of features from Chrome 81. This adds
  'ch-ua-mobile', removes 'document-access', and 'vr', and renames
  'downloads-without-user-activation' to 'downloads'.

3.2.0 (2020-01-19)
------------------

* Updated to the latest set of features from Chrome. This adds 2 new features:
  'document-access' and 'xr-spatial-tracking'. This also removes the 'speaker'
  since it has now been
  `removed from the w3c specification <https://github.com/w3c/webappsec-feature-policy/commit/18707d396e1d3f0be3de348fc432383cc8866e0b>`__.

3.1.0 (2019-11-15)
------------------

* Updated to the latest set of features from Chrome. This adds 17 new features:
  'ch-device-memory', 'ch-downlink', 'ch-dpr', 'ch-ect', 'ch-lang', 'ch-rtt',
  'ch-ua', 'ch-ua-arch', 'ch-ua-model', 'ch-ua-platform', 'ch-viewport-width',
  'ch-width', 'execution-while-not-rendered', and
  'execution-while-out-of-viewport'. Chrome has also removed support for
  'speaker' but since this is still in the specification, it has been left.
* Converted setuptools metadata to configuration file. This meant removing the
  ``__version__`` attribute from the package. If you want to inspect the
  installed version, use
  ``importlib.metadata.version("django-feature-policy")``
  (`docs <https://docs.python.org/3.8/library/importlib.metadata.html#distribution-versions>`__ /
  `backport <https://pypi.org/project/importlib-metadata/>`__).
* Suport Python 3.8.

3.0.0 (2019-08-02)
------------------

* Updated to the latest set of features from Chrome. This removes
  'legacy-image-formats' and 'unoptimized-images', and adds 17 new features:
  'downloads-without-user-activation', 'focus-without-user-activation',
  'forms', 'hid', 'idle-detection', 'loading-frame-default-eager', 'modals',
  'orientation-lock', 'pointer-lock', 'popups', 'presentation', 'scripts',
  'serial', 'top-navigation', 'unoptimized-lossless-images',
  'unoptimized-lossless-images-strict' and  'unoptimized-lossy-images'. Note
  that most of these are still experimental as can be seen on the [W3C feature
  list](https://github.com/w3c/webappsec-feature-policy/blob/master/features.md).

* Stop marking the distributed wheel as universal. Python 2 was never supported
  so the wheel was never actually universal.

2.3.0 (2019-05-19)
------------------

* Update Python support to 3.5-3.7, as 3.4 has reached its end of life.

* Make the generated header deterministic by iterating the settings dict in
  sorted order.

* Support Django 1.11 for completeness.

2.2.0 (2019-05-08)
------------------

* Fix interpretation of '*' by not automatically adding quotes.
* Optimize header generation to reduce impact on every request.

2.1.0 (2019-04-28)
------------------

* Tested on Django 2.2. No changes were needed for compatibility.

2.0.0 (2019-03-29)
------------------

* Updated to the latest set of features from Chrome.
  'animations', 'image-compression', and 'max-downscaling-image' have been
  removed, whilst 'document-domain', 'font-display-late-swap',
  'layout-animations', 'oversized-images', 'unoptimized-images', and
  'wake-lock' have been added.
  See more at https://github.com/w3c/webappsec-feature-policy/blob/master/features.md .

1.0.1 (2019-01-02)
------------------

* Support for new 'lazyload' feature, per https://www.chromestatus.com/feature/5641405942726656.

1.0.0 (2018-10-24)
------------------

* First release, supporting adding the header with a middleware.
