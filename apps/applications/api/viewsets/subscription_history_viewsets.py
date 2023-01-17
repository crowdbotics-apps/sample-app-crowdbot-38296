import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .. import serializers


class SubscriptionHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.SubscriptionHistorySerializer
    queryset = serializers.SubscriptionHistorySerializer.Meta.model.objects.get_queryset().select_related('app')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        app_pk = self.kwargs.get('app_id')

        try:
            uuid.UUID(app_pk)
        except ValueError:
            content = {'detail': [_('Invalid application.')]}
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)

        if app_pk:
            queryset = queryset.filter(app_id=app_pk)
        else:
            queryset = queryset.none()
        return queryset
