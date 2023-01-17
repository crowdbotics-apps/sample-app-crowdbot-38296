from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from ..constants import (
    PLAN_ACTION_TYPE_SUBSCRIBE,
    PLAN_ACTION_TYPE_SWITCH,
    PLAN_ACTION_TYPE_UNSUBSCRIBE,
    PLAN_ACTION_TYPE_UPGRADE,
    PLAN_ACTION_TYPE_DOWNGRADE,
)


class PlanActionType(TextChoices):
    SUBSCRIBE = PLAN_ACTION_TYPE_SUBSCRIBE, _('Subscribe')
    SWITCH = PLAN_ACTION_TYPE_SWITCH, _('Switch')
    UNSUBSCRIBE = PLAN_ACTION_TYPE_UNSUBSCRIBE, _('Unsubscribe')
    UPGRADE = PLAN_ACTION_TYPE_UPGRADE, _('Upgrade')
    DOWNGRADE = PLAN_ACTION_TYPE_DOWNGRADE, _('Downgrade')
