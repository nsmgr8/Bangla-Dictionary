from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html'}),
    (r'^account/', include('gaeauth.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^dictionary/', include('bangladict.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)
