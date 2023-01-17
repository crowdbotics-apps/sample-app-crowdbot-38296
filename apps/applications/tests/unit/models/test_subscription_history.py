from decimal import Decimal

from django.test import TestCase

from ... import factories
from .... import constants, models

SAMPLE_PRICE = Decimal(150.50)


class TestSubscriptionHistoryModel(TestCase):
    def test_prices_display__subscribe(self):
        """ Tests old price output """
        plan = factories.PlanFactory()

        history = models.SubscriptionHistory(
            action_type=constants.PLAN_ACTION_TYPE_SUBSCRIBE,
            current_plan_name=plan.name,
            current_price=plan.price,
            old_plan_name=None,
            old_price=None,
        )

        self.assertEqual(history.old_price_display, constants.PLAN_NAME_UNKNOWN)
        self.assertEqual(history.track_plan_price, f'{constants.PLAN_NAME_UNKNOWN} -> {plan.price}')

    def test_prices_display__upgrade(self):
        """ Tests old price output """
        plan = factories.PlanFactory()
        free_plan = factories.PlanFactory(price=Decimal(0))

        history = models.SubscriptionHistory(
            action_type=constants.PLAN_ACTION_TYPE_UPGRADE,
            current_plan_name=plan.name,
            current_price=plan.price,
            old_plan_name=free_plan.name,
            old_price=free_plan.price,  # 0.00
        )

        self.assertEqual(history.old_price_display, constants.PLAN_FREE)
        self.assertEqual(history.track_plan_price, f'{constants.PLAN_FREE} -> {plan.price}')

    def test_prices_display__downgrade(self):
        """ Tests old price output """
        plan = factories.PlanFactory()
        free_plan = factories.PlanFactory(price=Decimal(0))

        history = models.SubscriptionHistory(
            action_type=constants.PLAN_ACTION_TYPE_DOWNGRADE,
            current_plan_name=free_plan.name,
            current_price=free_plan.price,
            old_plan_name=plan.name,
            old_price=plan.price,  # 0.00
        )

        self.assertEqual(history.old_price_display, str(plan.price))
        self.assertEqual(history.track_plan_price, f'{plan.price} -> {constants.PLAN_FREE}')

    def test_prices_display__switch(self):
        plan1 = factories.PlanFactory()
        plan2 = factories.PlanFactory()

        # """ Tests old price output """
        history = models.SubscriptionHistory(
            action_type=constants.PLAN_ACTION_TYPE_SWITCH,
            current_plan_name=plan2.name,
            current_price=plan2.price,
            old_plan_name=plan1.name,
            old_price=plan1.price,  # 0.00
        )

        self.assertEqual(history.old_price_display, str(plan1.price))
        self.assertEqual(history.track_plan_price, f'{plan1.price} -> {plan2.price}')

