from django.conf.urls import patterns, include, url
from processregistry.registry.api import ProcessDefinitionResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

process_definition_resource = ProcessDefinitionResource()

urlpatterns = patterns('',

    (r'^api/', include(process_definition_resource.urls)),
    # Examples:
    # url(r'^$', 'processregistry.views.home', name='home'),
    # url(r'^processregistry/', include('processregistry.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
