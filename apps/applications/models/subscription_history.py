from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.applications.constants import PLAN_NAME_UNKNOWN_ALIAS, PLAN_NAME_UNKNOWN, PLAN_FREE
from apps.applications.enums import PlanActionType
from core.models import mixins


class CannotDeleteRule(mixins.DeletionRuleChecker):
    """ Rule sets that a subscription history must not be deleted. """

    def check(self, instance):
        raise mixins.RuleIntegrityError('Subscription history cannot be deleted.')


class SubscriptionHistory(mixins.UUIDPkMixin, mixins.DomainRuleMixin, models.Model):
    """
    Subscription tracks what plans an app has been associated. This is considered a non-transactional record, never
    edited, never deleted.
    """

    objects = mixins.RuleManager()

    deletion_rules = (
        CannotDeleteRule,
    )

    class Meta:
        verbose_name = _('subscription history')
        verbose_name_plural = _('subscription histories')
        ordering = ['created_at']


    app = models.ForeignKey(
        'applications.application',
        verbose_name=_('application'),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='histories',
    )

    old_plan_name = models.CharField(
        max_length=255,
        verbose_name=_('old plan name'),
        null=True,
        blank=True,
    )

    current_plan_name = models.CharField(
        max_length=255,
        verbose_name=_('current plan name'),
        null=True,
        blank=True,
    )

    action_type = models.CharField(
        max_length=11,
        null=False,
        blank=False,
        verbose_name=_('action type'),
        choices=PlanActionType.choices,
    )

    old_price = models.DecimalField(
        max_digits=8,
        null=True,
        blank=True,
        decimal_places=2,
        verbose_name=_('old price'),
    )

    current_price = models.DecimalField(
        max_digits=8,
        null=True,
        blank=True,
        decimal_places=2,
        verbose_name=_('current price'),
    )

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        null=False,
        blank=False,
        editable=False,
    )

    @property
    def old_price_display(self) -> str:
        if self.old_price is None:
            return PLAN_NAME_UNKNOWN
        return str(self.old_price) if self.old_price > 0 else PLAN_FREE

    @property
    def current_price_display(self) -> str:
        if self.current_price is None:
            return PLAN_NAME_UNKNOWN
        return str(self.current_price) if self.current_price > 0 else PLAN_FREE

    @property
    def track_plan_name(self) -> str:
        old_plan_name = self.old_plan_name or PLAN_FREE
        old_plan_name = PLAN_NAME_UNKNOWN if old_plan_name == PLAN_NAME_UNKNOWN_ALIAS else old_plan_name
        plan_name = self.current_plan_name or PLAN_FREE
        return f'{old_plan_name} -> {plan_name}'

    @property
    def track_plan_price(self) -> str:
        return f'{self.old_price_display} -> {self.current_price_display}'

    def __str__(self):
        price = self.current_price if self.current_price > 0 else 'free'
        return f'{self.current_plan_name} ({price}) {self.action_type}'
