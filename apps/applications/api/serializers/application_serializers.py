from rest_framework import serializers

from apps.users.api.serializers import SimpleUserSerializer
from core.serializers import FormSerializerMixin
from .plan_serializers import SimplePlanSerializer
from ... import forms


class ApplicationSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.ApplicationForm
        model = forms.ApplicationForm.Meta.model
        fields = (
            'id',
            'name',
            'type',
            'framework',
            'screenshot',
            'description',
            'domain_name',
            'active',
            'plan',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None
        super().__init__(*args, **kwargs)

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'user': self.user})
        return super().get_form(data=data, files=files, **kwargs)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if self.is_requested_field('user'):
            rep['user'] = SimpleUserSerializer(instance=instance.user).data

        if self.is_requested_field('plan'):
            rep['plan'] = SimplePlanSerializer(instance=instance.plan).data

        return rep
