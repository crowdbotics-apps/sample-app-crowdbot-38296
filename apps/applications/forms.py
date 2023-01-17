from decimal import Decimal

from django import forms

from apps.applications import models


class PlanForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = '__all__'

    def clean_price(self):
        value = self.cleaned_data.get('price', 0)
        if value <= 0:
            return 0
        return value


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = (
            'name',
            'type',
            'framework',
            'screenshot',
            'description',
            'domain_name',
            'active',
            'plan',
            'user',
        )
