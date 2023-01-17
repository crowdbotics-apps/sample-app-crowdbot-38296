from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


class Plan(mixins.UUIDPkMixin,
           mixins.ActivableMixin,
           mixins.DateTimeManagementMixin,
           mixins.EntityMixin,
           models.Model):
    """
    Plans to which a user can subscribe their app. Plans are billed on a monthly basis.
    Price can be 0.
    """

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')
        ordering = ['name']

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
        null=False,
        blank=False,
        help_text=_('Provide a name for the plan'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )

    price = models.DecimalField(
        max_digits=8,
        null=True,
        blank=True,
        decimal_places=2,
        verbose_name=_('price'),
    )

    def clean(self):
        self.price = self.price if self.price >= 0 else Decimal(0)
        super().clean()

    def __str__(self):
        return self.name
