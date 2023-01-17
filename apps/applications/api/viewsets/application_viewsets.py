from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class ApplicationViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    queryset = serializers.ApplicationSerializer.Meta.model.objects.get_queryset()
    filterset_fields = ('plan', 'active', 'plan__active',)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    lookup_url_kwarg = 'id'

    def get_serializer(self, *args, **kwargs):
        if hasattr(self.request, 'user') and kwargs.get('many', False) is False:
            kwargs.update({'user': self.request.user})
        return super().get_serializer(*args, **kwargs)
