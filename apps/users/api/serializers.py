from rest_framework import serializers

from .. import models


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'is_active',
        )
