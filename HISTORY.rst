History
=======

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
