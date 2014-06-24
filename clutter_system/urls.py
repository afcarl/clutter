from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'humansort.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('clutter.urls')),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':'images'}),
)

urlpatterns += staticfiles_urlpatterns()

