#
# Copyright 2010 BengDict Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from bangladict.models import Dictionary

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html',
      'extra_context': {'dict': Dictionary.objects.all}}),
    (r'^accounts/', include('gaeauth.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^dictionary/', include('bangladict.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^contributor/', include('contributor.urls')),
)
