import json

from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from processregistry.registry.models import ProcessDefinition


class ProcessDefinitionResource(ModelResource):
    class Meta:
        queryset = ProcessDefinition.objects.all()
        resource_name = 'process_definition'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def dehydrate_definition(self, bundle):
        return json.loads(bundle.data['definition'])

    def hydrate_definition(self, bundle):
        bundle.data['definition'] = json.dumps(bundle.data['definition'])
        return bundle
