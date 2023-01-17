from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class PlanViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.PlanSerializer
    queryset = serializers.PlanSerializer.Meta.model.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    lookup_url_kwarg = 'id'
