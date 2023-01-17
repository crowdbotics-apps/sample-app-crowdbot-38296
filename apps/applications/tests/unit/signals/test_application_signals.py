from decimal import Decimal
from django.test import TestCase

from ... import factories
from ....enums import PlanActionType
from ....models import SubscriptionHistory


class ApplicationSignalsTestCase(TestCase):
    def setUp(self) -> None:
        self.queryset = SubscriptionHistory.objects.get_queryset()

    def test_subscription_history__subscribe(self):
        """ Tests registration of a subscription history record when application subscribes to a plan """
        app = factories.ApplicationFactory(plan=None)
        self.assertEqual(self.queryset.count(), 0)

        plan = factories.PlanFactory()
        app.plan = plan
        app.save()

        self.assertEqual(self.queryset.count(), 1)
        history = self.queryset.last()

        self.assertEqual(history.app_id, app.pk)
        self.assertEqual(history.action_type, PlanActionType.SUBSCRIBE)
        self.assertEqual(history.current_price, plan.price)
        self.assertEqual(history.current_plan_name, plan.name)

    def test_subscription_history__unsubscribe(self):
        """ Tests registration of a subscription history record when application removes a plan """
        app = factories.ApplicationFactory()
        self.assertEqual(self.queryset.count(), 0)

        old_plan = app.plan
        app.plan = None
        app.save()

        self.assertEqual(self.queryset.count(), 1)
        history = self.queryset.last()

        self.assertEqual(history.app_id, app.pk)
        self.assertEqual(history.action_type, PlanActionType.UNSUBSCRIBE)
        self.assertEqual(history.old_plan_name, old_plan.name)
        self.assertEqual(history.old_price, old_plan.price)
        self.assertEqual(history.current_plan_name, None)
        self.assertEqual(history.current_price, None)

    def test_subscription_history__switch(self):
        """ Tests registration of subscription history record when application switches the plan """
        sample_price = Decimal(100)
        plan1 = factories.PlanFactory(price=sample_price)
        plan2 = factories.PlanFactory(price=sample_price)

        app = factories.ApplicationFactory(plan=plan1)
        self.assertEqual(self.queryset.count(), 0)

        app.plan = plan2
        app.save()

        self.assertEqual(self.queryset.count(), 1)
        history = self.queryset.last()

        self.assertEqual(history.app_id, app.pk)
        self.assertEqual(history.action_type, PlanActionType.SWITCH)
        self.assertEqual(history.old_plan_name, plan1.name)
        self.assertEqual(history.old_price, plan1.price)
        self.assertEqual(history.current_plan_name, plan2.name)
        self.assertEqual(history.current_price, plan2.price)

    def test_subscription_history__upgrade(self):
        """ Tests registration of subscription history record when application upgrades the plan """
        sample_price1 = Decimal(100)
        sample_price2 = Decimal(250)

        plan1 = factories.PlanFactory(price=sample_price1)
        plan2 = factories.PlanFactory(price=sample_price2)

        app = factories.ApplicationFactory(plan=plan1)
        self.assertEqual(self.queryset.count(), 0)

        app.plan = plan2
        app.save()

        self.assertEqual(self.queryset.count(), 1)
        history = self.queryset.last()

        self.assertEqual(history.app_id, app.pk)
        self.assertEqual(history.action_type, PlanActionType.UPGRADE)
        self.assertEqual(history.old_plan_name, plan1.name)
        self.assertEqual(history.old_price, plan1.price)
        self.assertEqual(history.current_plan_name, plan2.name)
        self.assertEqual(history.current_price, plan2.price)

    def test_subscription_history__downgrades(self):
        """ Tests registration of subscription history record when application downgrades the plan """
        sample_price1 = Decimal(250)
        sample_price2 = Decimal(100)

        plan1 = factories.PlanFactory(price=sample_price1)
        plan2 = factories.PlanFactory(price=sample_price2)

        app = factories.ApplicationFactory(plan=plan1)
        self.assertEqual(self.queryset.count(), 0)

        app.plan = plan2
        app.save()

        self.assertEqual(self.queryset.count(), 1)
        history = self.queryset.last()

        self.assertEqual(history.app_id, app.pk)
        self.assertEqual(history.action_type, PlanActionType.DOWNGRADE)
        self.assertEqual(history.old_plan_name, plan1.name)
        self.assertEqual(history.old_price, plan1.price)
        self.assertEqual(history.current_plan_name, plan2.name)
        self.assertEqual(history.current_price, plan2.price)
