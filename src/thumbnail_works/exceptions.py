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

class ImageSizeError(Exception):
    pass

class ThumbnailOptionError(Exception):
    pass

class ThumbnailWorksError(Exception):
    """Internal thumbnail_works error.
    
    Should be raised any time a method encounters an argument having a bad type
    or bad value. Write as many such checks as necessary in order to catch any
    changes in the underlying framework.
    
    This is important, since this app is built on Django internal structures,
    which might change without notice.
    
    """
    pass

class NoAccessToImage(Exception):
    pass
