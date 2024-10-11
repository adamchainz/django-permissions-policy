=========
Changelog
=========

4.22.0 (2024-10-11)
-------------------

* Updated to the latest set of features from Chrome 131 dev.

  New features:

  * ``popins``
  * ``web-app-installation``

* Drop Python 3.8 support.

* Support Python 3.13.

4.21.0 (2024-08-08)
-------------------

* Updated to the latest set of features from Chrome 129 dev.

  New features:

  * ``captured-surface-control``
  * ``ch-ua-form-factors`` (renamed from ``ch-ua-form-factor``)
  * ``deferred-fetch``
  * ``digital-credentials-get``

  Removed features:

  * ``ch-ua-form-factor``
  * ``direct-sockets``
  * ``usb-unrestricted``

4.20.0 (2024-06-19)
-------------------

* Support Django 5.1.

4.19.0 (2024-01-21)
-------------------

* Fix ASGI compatibility on Python 3.12.

  Thanks to Alexandre Spaeth in `PR #426 <https://github.com/adamchainz/django-permissions-policy/pull/426>`__.

* Updated to the latest set of features from Chrome 122 dev.

  New features:

  - ``publickey-credentials-create``
  - ``usb-unrestricted``

4.18.0 (2023-10-09)
-------------------

* Support Django 5.0.

* Updated to the latest set of features from Chrome 119 dev.

  New features:

  * ``browsing-topics``
  * ``ch-prefers-reduced-transparency``
  * ``ch-ua-form-factor``
  * ``interest-cohort``
  * ``join-ad-interest-group``
  * ``private-aggregation``
  * ``private-state-token-issuance``
  * ``private-state-token-redemption``
  * ``run-ad-auction``
  * ``shared-storage``
  * ``shared-storage-select-url``
  * ``window-management``

4.17.0 (2023-07-10)
-------------------

* Drop Python 3.7 support.

4.16.0 (2023-06-14)
-------------------

* Support Python 3.12.

4.15.0 (2023-02-25)
-------------------

* Support Django 4.2.

* Updated to the latest set of features from Chrome 111 dev.

  New features:

  - ``identity-credentials-get``
  - ``storage-access``

4.14.0 (2022-11-30)
-------------------

* Updated to the latest set of features from Chrome 109 dev.

  New features:

  - ``ch-prefers-reduced-motion``
  - ``compute-pressure``
  - ``direct-sockets``
  - ``unload``

  Removed features:

  - ``ch-partitioned-cookies``

4.13.0 (2022-08-12)
-------------------

* Add async support to the middleware, to reduce overhead on async views.

4.12.0 (2022-06-05)
-------------------

* Support Python 3.11.

* Support Django 4.1.

4.11.0 (2022-05-27)
-------------------

* Updated to the latest set of features from Chrome 104 dev.

  New features:

  - ``bluetooth``
  - ``ch-save-data``
  - ``local-fonts``

* Restore ``interest-cohort`` feature and recommend disabling it in README.
  The original API, FLoC, was removed from Chrome, but there’s a replacement proposal `The Topics API <https://github.com/patcg-individual-drafts/topics>`__.
  The proposal states that the ``interest-cohort`` feature will be recognized to disable it.

4.10.0 (2022-05-10)
-------------------

* Drop support for Django 2.2, 3.0, and 3.1.

4.9.0 (2022-03-25)
------------------

* Updated to the latest set of features from Chrome 100 dev.

  New features:

  - ``ch-partitioned-cookies``

4.8.0 (2022-02-16)
------------------

* Updated to the latest set of features from Chrome 100 dev.

  New features:

  - ``ch-ua-wow64``

  Removed features:

  - ``interest-cohort``

4.7.0 (2022-01-10)
------------------

* Drop Python 3.6 support.

4.6.0 (2021-12-29)
------------------

* Updated to the latest set of features from Chrome 98 dev.

  New features:

  - ``ch-ua-full-version-list``
  - ``keyboard-map``

4.5.0 (2021-10-06)
------------------

* Updated to the latest set of features from Chrome 96 dev and Firefox 93.

  New features:

  - ``ch-viewport-height``
  - ``speaker-selection``

  Removed features:

  - ``ch-lang``
  - ``ch-ua-reduced``
  - ``shared-autofill``
  - ``speaker``

4.4.0 (2021-10-05)
------------------

* Support Python 3.10.

4.3.0 (2021-09-28)
------------------

* Support Django 4.0.

4.2.0 (2021-08-07)
------------------

* Updated to the latest set of features from Chrome 94 dev.

  New features:

  - ``ch-ua-bitness``
  - ``ch-ua-reduced``

* Add type hints.

4.1.0 (2021-06-02)
------------------

* Updated to the latest set of features from Chrome 92 dev.

  New features:

  - ``attribution-reporting``
  - ``ch-prefers-color-scheme``
  - ``shared-autofill``
  - ``window-placement``

  Removed features:

  - ``conversion-tracking``

4.0.1 (2021-05-02)
------------------

* Improve setup instructions.

4.0.0 (2021-03-24)
------------------

* Rename the package from ``django-feature-policy`` to
  ``django-permissions-policy`` and the module name from
  ``django_feature_policy`` to ``django_permissions_policy`` accordingly.

* Stop sending the ``Feature-Policy`` header. Chrome now logs warnings if it is
  sent alongside ``Permissions-Policy``.

* Remove support for the legacy setting name ``FEATURE_POLICY`` and the old
  middleware alias ``FeaturePolicyMiddleware``.

* Stop distributing tests to reduce package size. Tests are not intended to be
  run outside of the tox setup in the repository. Repackagers can use GitHub's
  tarballs per tag.

3.8.0 (2021-03-13)
------------------

* Updated to the latest set of features from Chrome 91 dev.

  New features:

  - ``conversion-measurement``
  - ``interest-cohort``
  - ``otp-credentials``

  Removed features:

  - ``document-write``
  - ``downloads``
  - ``forms``
  - ``modals``
  - ``orientation-lock``
  - ``pointer-lock``
  - ``popups``
  - ``presentation``
  - ``scripts``
  - ``sync-script``
  - ``top-navigation``

3.7.0 (2021-01-25)
------------------

* Support Django 3.2.

3.6.0 (2020-12-13)
------------------

* Drop Python 3.5 support.
* Support Python 3.9.

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
