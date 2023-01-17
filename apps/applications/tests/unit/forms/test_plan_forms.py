from decimal import Decimal
from django.test import TestCase

from apps.applications.forms import PlanForm


class PlanFormTestCase(TestCase):
    def test_force_zero_when_price_is_negative(self):
        """ Tests price to force it as zero if value provided is negative. """
        data = {
            'price': Decimal(-100),
        }
        form = PlanForm(data=data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.cleaned_data.get('price'), Decimal(0))

        data = {
            'price': Decimal(100),
        }
        form = PlanForm(data=data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.cleaned_data.get('price'), data.get('price'))


