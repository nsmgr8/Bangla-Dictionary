from django.conf.urls.defaults import *

urlpatterns = patterns('bangladict.views',
    url(r'^$', 'dictionary_list', name='dict_list'),
    url(r'^(?P<dict_abbrev>\w+)/$', 'word_list', name='dict_word_list'),
    url(r'^comments/(?P<wid>\w+)/$', 'word_comments', name='dict_word_comments'),
    url(r'^word/(?P<dict_abbrev>\w+)/(?P<word>.+)/$', 'word_detail', name='dict_word_detail'),
)

