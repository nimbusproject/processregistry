import json

from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource

from processregistry.registry.models import ProcessDefinition
from processregistry.auth import UserObjectsOnlyAuthorization


class ProcessDefinitionResource(ModelResource):

    class Meta:
        queryset = ProcessDefinition.objects.all()
        resource_name = 'process_definition'
        authorization = UserObjectsOnlyAuthorization()
        authentication = BasicAuthentication()

    def obj_create(self, bundle, **kwargs):
        print "Creating with"
        return super(ProcessDefinitionResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        print "LIMIT"
        print request.user
        return object_list.filter(user=request.user)

    def dehydrate_definition(self, bundle):
        return json.loads(bundle.data['definition'])

    def hydrate_definition(self, bundle):
        bundle.data['definition'] = json.dumps(bundle.data['definition'])
        return bundle
