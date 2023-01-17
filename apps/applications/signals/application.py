from django.db.models.signals import post_save
from django.dispatch import receiver

from ..constants import PLAN_NAME_UNKNOWN_ALIAS
from ..enums import PlanActionType
from ..models import Application, Plan, SubscriptionHistory


@receiver(post_save, sender=Application)
def register_subscription_history(instance: Application, raw: bool, **_) -> None:
    if raw is True:
        # fixtures inserted are ignored
        return

    if instance.has_changed('plan_id') is False:
        # Nothing changed
        return

    old_plan_id = instance.old_value('plan_id')

    if not old_plan_id and not instance.plan_id:
        # Plan changed, there is no current plan and old plan is not found
        # do nothing
        return

    history = SubscriptionHistory(app_id=instance.pk)
    old_plan = None

    if old_plan_id:
        if old_plan_id == instance.plan_id:
            # False positive
            # Do nothing
            return

        try:
            old_plan = Plan.objects.get(pk=old_plan_id)
            history.old_plan_name = old_plan.name
            history.old_price = old_plan.price

        except Plan.DoesNotExist:
            # current plan exists, old plan is present but no longer found in persistence
            # Let's consider it as subscription switch.
            history.action_type = PlanActionType.SWITCH
            history.old_plan_name = PLAN_NAME_UNKNOWN_ALIAS

    else:
        # Plan changed and there no previous plan
        history.action_type = PlanActionType.SUBSCRIBE

    if instance.plan_id:
        plan = instance.plan
        history.current_plan_name = plan.name
        history.current_price = plan.price

        if old_plan:
            if plan.price < old_plan.price:
                history.action_type = PlanActionType.DOWNGRADE
            elif plan.price == old_plan.price:
                history.action_type = PlanActionType.SWITCH
            elif plan.price > old_plan.price:
                history.action_type = PlanActionType.UPGRADE

    elif old_plan_id:
        # Plan changed, there is no current plan and old plan exists
        history.action_type = PlanActionType.UNSUBSCRIBE

    history.validate()
    history.save()
