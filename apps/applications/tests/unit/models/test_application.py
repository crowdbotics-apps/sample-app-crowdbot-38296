from decimal import Decimal
from django.test import TestCase

from ... import factories


class TestApplicationModelTestCase(TestCase):
    def setUp(self) -> None:
        self.free_plan = factories.PlanFactory(price=None)

    def test_free_flag(self):
        """ Tests free property whether it is true when price is 0 """
        app = factories.ApplicationFactory(plan=None)
        self.assertEqual(app.free, True)

        plan = factories.PlanFactory()
        self.assertIsNotNone(plan.price)

        app.plan = plan
        self.assertEqual(app.free, False)

        free_plan = factories.PlanFactory(price=None)
        self.assertIsNone(free_plan.price)

        app.plan = free_plan
        self.assertEqual(app.free, True)

        free_plan = factories.PlanFactory(price=Decimal(0))
        self.assertEqual(free_plan.price, Decimal(0))

        app.plan = free_plan
        self.assertEqual(app.free, True)

    def test_track_plan_changes(self):
        """ Tests whether plan is tracked in model when it is changed. """
        app = factories.ApplicationFactory(plan=None)
        self.assertIsNone(app.old_value('plan_id'))
        self.assertEqual(app.has_changed('plan_id'), False)

        plan = factories.PlanFactory()
        app.plan = plan
        app.save()  # Let's store plan

        free_plan = factories.PlanFactory(price=None)
        app.plan = free_plan

        # Old value is not the current free plan, but the first one persisted
        self.assertEqual(app.has_changed('plan_id'), True)
        self.assertEqual(app.old_value('plan_id'), plan.pk)
