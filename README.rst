django-thumbnail-works
========================================================================

NOTICE: This is fork of orginal project

| **Author**: `George Notaras <http://www.g-loaded.eu/>`_
| **Development Web Site**: `django-thumbnail-works project <http://www.codetrax.org/projects/django-thumbnail-works>`_
| **Source Code Repository**: `django-thumbnail-works source code <https://source.codetrax.org/hgroot/django-thumbnail-works>`_
| **Documentation**: `django-thumbnail-works documentation <http://packages.python.org/django-thumbnail-works>`_
| **Downloads**: `django-thumbnail-works releases <http://pypi.python.org/pypi/django-thumbnail-works>`_

*django-thumbnail-works* provides an enhanced ImageField that generates and
manages thumbnails of the source image.

This application aims to be a simple but feature rich thumbnailing
application for Django based projects.

Licensed under the *Apache License version 2.0*. More licensing information
exists in the license_ section.

**Warning**: This software is not production-ready!


Features
========

- Provides the ``EnhancedImageField`` model field, which is based on the
  default Django ``ImageField``, and has the ability to generate and manage
  thumbnails of the source image.
- Supports *named* thumbnails which can be accessed as attributes of the
  source image.
- Uses the Django storages API to manage thumbnails.
- Allows processing the source image in the same manner that thumbnails are
  processed.
- Individual processing options for each thumbnail.
- Supports automatic image resizing and cropping to the user specified size.
  Scaling up smaller images is also possible.
- *Sharpen* and *detail* filters.
- You can specify the output format of each image, including the format of the
  source image.
- Supports delayed thumbnail generation, which means that thumbnails are
  generated the first time they are accessed.

Thumbnail generation using template tags is not supported and there are
no plans to support it in the near future. The logic of this application
is to define *named* thumbnails and access them as attributes of the source
image. This way you only need to create your own template tags that display
the thumbnails in any way you see fit.


Documentation
=============

Apart from the `django-thumbnail-works Online Documentation`_, more information about the
installation, configuration and usage of this application may be available
at the project's wiki_.

.. _`django-thumbnail-works Online Documentation`: http://packages.python.org/django-thumbnail-works
.. _wiki: http://www.codetrax.org/projects/django-thumbnail-works/wiki


Donations
=========

This software is released as free-software and provided to you at no cost. However,
a significant amount of time and effort has gone into developing this software
and writing this documentation. So, the production of this software has not
been free from cost. It is highly recommended that, if you use this software
*in production*, you should consider making a donation.

To make a donation, please visit the CodeTRAX `donations page`_ which contains
a PayPal_ *donate* button.

Thank you for considering making a donation to django-thumbnail-works.

.. _`donations page`: https://source.codetrax.org/donate.html
.. _PayPal: https://www.paypal.com


Bugs and feature requests
=========================

In case you run into any problems while using this application or think that
a new feature should be implemented, it is highly recommended you submit_ a new
report about it at the project's `issue tracker`_.

Using the *issue tracker* is the recommended way to notify the authors about
bugs or make feature requests. Also, before submitting a new report, please
make sure you have read the `new issue guidelines`_.

.. _submit: http://www.codetrax.org/projects/django-thumbnail-works/issues/new
.. _`issue tracker`: http://www.codetrax.org/projects/django-thumbnail-works/issues
.. _`new issue guidelines`: http://www.codetrax.org/NewIssueGuidelines


Support
=======

CodeTRAX does not provide support for django-thumbnail-works.

You can still get community support at the `Community Support Forums`_:

.. _`Community Support Forums`: http://www.codetrax.org/projects/django-thumbnail-works/boards


License
=======

Copyright 2010 George Notaras <gnot [at] g-loaded.eu>

Licensed under the *Apache License, Version 2.0* (the "*License*");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the License exists in the product distribution; the *LICENSE* file.
For copyright and other important notes regarding this release please read
the *NOTICE* file.
