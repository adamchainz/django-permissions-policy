History
=======

Pending release
---------------

.. Insert new release notes below this line

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
