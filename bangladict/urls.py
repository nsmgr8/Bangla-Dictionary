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

urlpatterns = patterns('bangladict.views',
    url(r'^$', 'dictionary_list', name='dict_list'),
    url(r'^(?P<dict_abbrev>\w+)/$', 'word_list', name='dict_word_list'),
    url(r'^comments/(?P<wid>\w+)/$', 'word_comments', name='dict_word_comments'),
    url(r'^(?P<dict_abbrev>\w+)/edit/create/$', 'word_edit', name='dict_word_create'),
    url(r'^(?P<dict_abbrev>\w+)/edit/(?P<wid>\d+)/$', 'word_edit', name='dict_word_edit'),
    url(r'^word/(?P<dict_abbrev>\w+)/(?P<word>.+)/$', 'word_detail', name='dict_word_detail'),
    url(r'^bulk/load/$', 'bulk_load', name='dict_bulk_load'),
)

