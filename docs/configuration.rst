
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-thumbnail-works* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


Configuring your project
========================

In the Django project's ``settings`` module, add ``thumbnail_works`` to the
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'thumbnail_works',
    )


Reference of the application settings
=====================================

The following settings can be specified in the Django project's ``settings``
module to customize the functionality of *django-thumbnail-works*.

``THUMBNAILS_FORMAT``
    If an image format is not specified in the thumbnail definition, this
    format is used to save the thumbnails or the original imageare (if it is
    processed). Valid values are any image formats supported by PIL. For
    instance, JPEG, PNG etc.

``THUMBNAILS_QUALITY``
    This setting accepts an integer that represents the quality parameter
    when saving JPEG images. It is not used for other image formats.

``THUMBNAILS_DIRNAME``
    This is the name of the directory where thumbnails are stored. By default,
    this is set to ``thubs``, which means that the thumbnails are saved in the
    ``<media_root>/<upload_to>/thumbs/`` directory.

``THUMBNAILS_DELAYED_GENERATION``
    If this setting is set to True (the default), thumbnails are generated
    the first time they are accessed. If this is set to False, then all
    thumbnails are generated as soon as the original image is uploaded.
    
