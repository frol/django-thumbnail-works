# -*- coding: utf-8 -*-
#
#  This file is part of django-thumbnail-works.
#
#  django-thumbnail-works adds thumbnail support to the default ImageField.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-thumbnail-works
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-thumbnail-works
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from django.db.models.fields.files import ImageField, ImageFieldFile
from django.utils.encoding import smart_unicode

from thumbnail_works.exceptions import ThumbnailOptionError
from thumbnail_works.exceptions import ThumbnailWorksError
from thumbnail_works import settings
from thumbnail_works.images import ImageProcessor



class BaseThumbnailFieldFile(ImageFieldFile):
    """A derived class of Django's ImageFieldFile for thumbnails.
    
    Note that this class cannot be used on its own, but also requires
    ``thumbnail_works.images.ImageProcessor`` or a derived class to
    provide the image processing methods.
    
    """
        
    def __init__(self, instance, field, source, name, identifier, proc_opts):
        """Constructor
        
        ``instance``
            The instance of the model that contains the ``EnhancedImageField``.
        ``field``
            The instance of the ``EnhancedImageField``.
        ``source``
            The instance of the ``EnhancedImageFieldFile`` of the source image.
        ``name``
            the name of the source image. Needs to pass through
            ``generate_image_name()`` to get a name for the thumbnail.
        ``identifier``
            the thumbnail identifier as set in the ``thumbnails`` dictionary.
        ``proc_opts``
            image processing options for this thumbnail as set in the
            ``thumbnails`` dictionary.
        
        The ``name`` attribute cannot be empty. By default, ``name`` contains
        a path relative to MEDIA_ROOT, eg: ``myimages/image1.png`` and is
        mandatory in order to have thumbnail management.
        
        """
        if not name:
            raise ThumbnailWorksError('The provided name is not usable: "%s"')
        
        # Set the thumbnail identifier
        self.identifier = self.get_identifier(identifier)
        # Set the image processing options for this image (thumbnail)
        self.setup_image_processing_options(proc_opts)
        self.source = source
        
        # Get a proper thumbnail name (relative path to MEDIA_ROOT)
        name = self.generate_image_name(name=name)
        # self.name is set by the following 
        super(BaseThumbnailFieldFile, self).__init__(instance, field, name)
    
    def get_identifier(self, identifier):
        if not isinstance(identifier, str):
            raise ThumbnailOptionError('The identifier must be a string')
        elif identifier == '':
            raise ThumbnailOptionError('The identifier must be set to something on thumbnails')
        return identifier.replace(' ', '_')
    
    def save(self, source_content=None):
        """Saves the thumbnail file.
        
        ``source_content``
            The image data of the source image
        
        Also sets the current object (thumbnail) as an attribute of the
        source image's ImageFieldFile.
        
        """
        if source_content is None:
            source_content = self.source.get_image_content()
            
        thumbnail_content = self.process_image(source_content)
        self.name = self.storage.save(self.name, thumbnail_content)
        
        # Set the thumbnail as an attribute of the source image's ImageFieldFile
        setattr(self.source, self.identifier, self)

        # Update the filesize cache
        self._size = len(thumbnail_content)
        
        self._committed = True

    def delete(self):
        """Deletes the thumbnail file.
        
        Also deletes the current object (thumbnail) from source image's
        ImageFieldFile object.
        
        """
        # Only close the file if it's already open, which we know by the
        # presence of self._file
        if hasattr(self, '_file'):
            self.close()
            del self.file

        self.storage.delete(self.name)

        self.name = None
        
        # Clear the thumbnail attribute on the source image file
        if hasattr(self.source, self.identifier):
            delattr(self.source, self.identifier)

        # Clear the image dimensions cache
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        
        # Delete the filesize cache
        if hasattr(self, '_size'):
            del self._size
        
        self._committed = False


class ThumbnailFieldFile(BaseThumbnailFieldFile, ImageProcessor):
    """An ImageFieldFile with image processing capabilities for thumbnails."""



class BaseEnhancedImageFieldFile(ImageFieldFile):
    """Enhanced version of the default ImageFieldFile for the source image.
    
    Note that this class cannot be used on its own, but also requires
    ``thumbnail_works.images.ImageProcessor`` or a derived class to
    provide the image processing methods.
    
    The BaseEnhancedImageFieldFile supports:
    
    - resizing the original image before saving it to the specified storage.
    - generating thumbnails of the original image on the same storage:
        - immediately after the original image is uploaded.
        - delayed generation when each thumbnail is accessed for the first time.
    - deleting the previously generated thumbnails from the specified storage.
    - a mechanism of accessing the thumbnails as attributes of the model's
      EnhancedImageField.
    
    """
    
    def __init__(self, instance, field, name):
        """Constructor
        
        ``instance``
            The instance of the model that contains the ``EnhancedImageField``.
        ``field``
            The instance of the ``EnhancedImageField``.
        ``name``
            the path of the file including the relative path from MEDIA_ROOT
            and the actual filename.
        
        Note that the ``name`` attribute is re-set to the name (relative path)
        of the image on the storage once the ``save()`` method has been called.
        
        The following ``BaseEnhancedImageFieldFile`` instance attributes are
        set by ``ImageFieldFile.__init__()``:
         
        ``storage``
            The ``storage`` attribute of the EnhancedImageField instance.
        ``_committed``
            boolean attribute that indicates whether the file object
            has been committed to the database and therefore saved to the
            storage or the file has been deleted from the database and therefore
            deleted from the filesystem.
        
        Thumbnails are set as attributes of the ``BaseEnhancedImageFieldFile``
        object (source image) only if they exist on the storage.
        
        If the thumbnail files are not found on the storage at this time, they
        will be generated the first time they are accessed regardless of the
        THUMBNAILS_DELAYED_GENERATION ``setting``.
        
        """
        # Set the identifier to None. Only thumbnails have an identifier attribute
        self.identifier = None
        # Set the image processing options for this image (source image)
        self.setup_image_processing_options(field.process_source)
        
        # Among others, also sets ``self.name``
        super(BaseEnhancedImageFieldFile, self).__init__(instance, field, name)
        
        # Set thumbnail objects as attributes.
        if self._verify_thumbnail_requirements():
            for identifier, proc_opts in self.field.thumbnails.items():
                t = ThumbnailFieldFile(self.instance, self.field, self, self.name, identifier, proc_opts)
                if self.storage.exists(smart_unicode(t.name)):
                    setattr(self, identifier, t)
    
    def _verify_thumbnail_requirements(self):
        """This function performs a series of checks to ensure flawless
        thumbnail access, generation and management. It is a safety mechanism.
        
        Before using instanciating ``ThumbnailFieldFile`` you should run
        this check. For example:
        
            if self._verify_thumbnail_requirements():
                t = ThumbnailFieldFile(...)
        
        """
        if not self._committed:
            # TODO: documentation for this check
            return False
        elif not self.field.thumbnails:
            # Check that a dictionary of *thumbnail definitions* has been set
            # on the field.
            return False
        elif not self.name:
            # Checks whether ``self.name`` (image path relative to MEDIA_ROOT)
            # has been set. A 'name' is required for thumbnail management.
            return False
        return True
        
    def __getattr__(self, attribute):
        """Retrieves any ``BaseEnhancedImageFieldFile`` instance attribute.
        
        If a thumbnail attribute is requested, but it has not been set as
        an ``BaseEnhancedImageFieldFile`` instance attribute, then:
        
        1. Generate the thumbnail
        2. Set it as an ``BaseEnhancedImageFieldFile`` instance attribute
        
        Developer Notes
        
        Here we use the ``BaseEnhancedImageFieldFile`` instance's __dict__ in
        order to check or set the instance's attributes so as to avoid
        triggering a recursive call to this function.
        
        A good write-up on this exists at:  http://bit.ly/c2JL8H
        
        """
        if not self.__dict__.has_key(attribute):
            # Proceed to thumbnail generation only if a *thumbnail* attribute
            # is requested
            if self.field.thumbnails.has_key(attribute):
                # Generate thumbnail
                self._require_file()    # TODO: document this
                if self._verify_thumbnail_requirements():
                    proc_opts = self.field.thumbnails[attribute]
                    t = ThumbnailFieldFile(self.instance, self.field, self, self.name, attribute, proc_opts)
                    t.save()
                    assert self.__dict__[attribute] == t, \
                        Exception('Thumbnail attribute `%s` not set' % attribute)
        return self.__dict__[attribute]
    
    def save(self, name, content, save=True):
        """Saves the source image and generates thumbnails.
        
        ``name``
            The name of the file including the relative path from MEDIA_ROOT.
        ``content``
            The file data.
        
        If the image processing options have been set, then the source image
        is processed before it is finally saved to the storage.
        
        After the source file is saved, if the ``THUMBNAILS_DELAYED_GENERATION``
        setting has been enabled, no thumbnails are generated. The thumbnails
        will be generated the first time they are accessed.
        
        If ``THUMBNAILS_DELAYED_GENERATION`` is set to False, then all thumbnails
        are generated as soon as the source image is saved.
        
        """
        
        # Resize the source image if image processing options have been set
        if self.proc_opts is not None:
            content = self.process_image(content)
            # The following sets the correct filename extension according
            # to the image format. 
            name = self.generate_image_name(name=name)
        
        # Save the source image on the storage.
        # This also re-sets ``self.name``
        super(BaseEnhancedImageFieldFile, self).save(name, content, save)
        
        if settings.THUMBNAILS_DELAYED_GENERATION:
            # Thumbnails will be generated on first access
            return
        
        # Generate all thumbnails
        if self._verify_thumbnail_requirements():
            for identifier, proc_opts in self.field.thumbnails.items():
                t = ThumbnailFieldFile(self.instance, self.field, self, self.name, identifier, proc_opts)
                t.save(content)
    
    def delete(self, save=True):
        """Deletes the thumbnails and the source image.
        
        If the files are missing from the storage, no errors are raised.
        
        """
        # First try to delete the thumbnails
        if self._verify_thumbnail_requirements():
            for identifier, proc_opts in self.field.thumbnails.items():
                t = ThumbnailFieldFile(self.instance, self.field, self, self.name, identifier, proc_opts)
                t.delete()
        
        # Delete the source file
        super(BaseEnhancedImageFieldFile, self).delete(save)


class EnhancedImageFieldFile(BaseEnhancedImageFieldFile, ImageProcessor):
    """
    Each of the thumbnails that have been specified in the ``thumbnails``
    dictionary are eventually set as attributes of the source image object.
    Each thumbnail's identifier is used as the name of the attribute.
    
    For example, the *avatar* thumbnail of a *photo* field, would be
    accessed as::
    
        photo.avatar
    
    Thumbnails inherit all the attributes of Django's ``ImageFieldFile``
    as described in the `file objects`_ documentation.
    
    .. _`file objects`: http://docs.djangoproject.com/en/1.2/ref/files/file/
    
    For instance, you can do something like the following in your templates::
    
        <img src="{{ photo.avatar.url }}"
            width="{{ photo.avatar.width }}"
            height="{{ photo.avatar.height }}"
            alt='{{ user.name }}' />
    
    """


class EnhancedImageField(ImageField):
    """This model field is an enhanced version of Django's ``ImageField``.
    
    *django-thumbnail-works* provides an enhanced version of the default Django's
    ``ImageField``, which supports:
    
    - Processing the original image before it is saved on the remote server.
    - Generating thumbnails of the source image and a mechanism of accessing
      the thumbnails as attributes of the source image.
    
    The ``EnhancedImageField`` derives from the default ``ImageField`` and thus
    all attributes and methods of the default ``ImageField`` are inherited.
    
    In addition to the default arguments, the ``EnhancedImageField`` also
    supports the following:
    
    ``process_source``
        A dictionary of *image processing options*. The same options, that can
        be used for the thumbnail generation, can also be set in this attribute.
        If this is set, the original image will be processed using the provided
        options before it is saved on the remote server. Contrariwise, if this
        attribute is not set or set to ``None``, the uploaded image is saved in
        its original form, without any further processing. It should be noted that
        setting this attribute to an empty dictionary still causes the source
        image to be processed using default image processing options. This
        practically means that the source image will be saved in the format
        specified by the ``THUMBNAILS_FORMAT`` setting without any resizing or
        filtering taking place.
    ``thumbnails``
        A dictionary of *thumbnail definitions*. The format of each thumbnail
        definition is::
    
            <thumbnail_identifier> : <image_processing_options>
        
        **thumbnail_identifier**
            Is a string that uniquely identifies the thumbnail. It is required
            that all thumbnails use a unique identifier. This identifier is used
            in the thumbnail access mechanism and is also used in the
            generated filename of the thumbnail image file.
        **image_processing_options**
            This is a dictionary of options that will be used during the thumbnail
            generation. This dictionary must be present on every thumbnail
            definition. Any of the following supported options may be used:
            
            ``size``
                A string of the format ``WIDTHxHEIGHT`` which represents the
                size of the generated thumbnail.
            ``sharpen``
                Boolean option. If set, the ``ImageFilter.SHARPEN`` filter will
                be applied to the thumbnail.
            ``detail``
                Boolean option. If set, the ``ImageFilter.DETAIL`` filter will
                be applied to the thumbnail.
            ``upscale``
                Boolean option. By default, image resizing occurs only if
                any of the source image dimensions is bigger than the dimension
                indicated by the ``size`` option. If the ``upscale`` option is
                set to ``True``, resizing occurs even if the generated thumbnail
                is bigger than the source image.
            ``format``
                This is the format in which the thumbnail should be saved.
                Valid values are those supported by the *Python Imaging Library*
                (PIL). If it is not set, then the default format specified by
                the ``THUMBNAILS_FORMAT`` setting will be used. In case the
                format is set to ``JPEG``, the value of the ``THUMBNAILS_QUALITY``
                is used as the quality when the image is saved.
    
    The following code snippet illustrates how to use the ``EnhancedImageField``::

        from django.db import models
        from thumbnail_works.fields import EnhancedImageField
        
        class MyModel(models.Model):
            photo = EnhancedImageField(
                upload_to = 'attachments/images',
                process_source = dict(
                    size='512x384', sharpen=True, upscale=True, format='JPEG'),
                thumbnails = {
                    'avatar': dict(size='80x60'),
                    'medium': dict(size='256x192', detail=True),
                }
            )
    
    """
    attr_class = EnhancedImageFieldFile
    
    def __init__(self, process_source=None, thumbnails={}, **kwargs):
        self.process_source = process_source
        self.thumbnails = thumbnails
        super(EnhancedImageField, self).__init__(**kwargs)

