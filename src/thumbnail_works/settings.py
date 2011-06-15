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

from django.conf import settings


# Anything supported by PIL
THUMBNAILS_FORMAT = getattr(settings, 'THUMBNAILS_FORMAT', 'JPEG')

# For JPEG format only
THUMBNAILS_QUALITY = getattr(settings, 'THUMBNAILS_QUALITY', 85)

# This is the name of the directory where the thumbnails will be stored
THUMBNAILS_DIRNAME = getattr(settings, 'THUMBNAILS_DIRNAME', 'thumbs')

# Generate the thumbnails on first access rather than at the time the
# original image is saved. 
THUMBNAILS_DELAYED_GENERATION = getattr(settings, 'THUMBNAILS_DELAYED_GENERATION', True)
