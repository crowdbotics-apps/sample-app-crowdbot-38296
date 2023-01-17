from rest_framework import serializers

from core.serializers import FormSerializerMixin
from ... import forms


class SimplePlanSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.PlanForm
        model = forms.PlanForm.Meta.model
        fields = (
            'id',
            'name',
            'price',
            'active',
        )


class PlanSerializer(SimplePlanSerializer):
    class Meta(SimplePlanSerializer.Meta):
        fields = SimplePlanSerializer.Meta.fields + (
            'description',
            'created_at',
            'updated_at',
        )
