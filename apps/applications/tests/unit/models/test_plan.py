from decimal import Decimal

from django.test import TestCase

from ... import factories


class TestPlanModel(TestCase):
    def test_force_zero_when_price_is_negative(self):
        """ Tests price to force it as zero if value provided is negative. """
        plan = factories.PlanFactory.build()
        plan.price = Decimal(-100)

        self.assertEqual(plan.price, Decimal(-100))

        plan.clean()
        self.assertEqual(plan.price, Decimal(0))
