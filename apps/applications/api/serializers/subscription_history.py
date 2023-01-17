from rest_framework import serializers

from ...models import SubscriptionHistory


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionHistory
        fields = (
            'id',
            'action_type',
            'old_plan_name',
            'current_plan_name',
            'old_price',
            'current_price',
            'created_at',
        )
