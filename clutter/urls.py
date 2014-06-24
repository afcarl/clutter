from django.conf.urls import patterns, url

from clutter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/(?P<item_id>[0-9]+)$', views.new, name='new'),
    url(r'^split/(?P<node_id>[0-9]+)$', views.split, name='split'),
    url(r'^merge$', views.merge, name='merge'),
    url(r'^visualize$', views.visualize, name='visualize'),
    url(r'^tree.json$', views.tree, name='tree'),
    url(r'^cloud/(?P<node_id>[0-9]+).json$', views.cloud, name='cloud'),
    url(r'^insert/(?P<item_id>[0-9]+)/(?P<node_id>[0-9]+)$', views.insert,
        name='insert'),
)

