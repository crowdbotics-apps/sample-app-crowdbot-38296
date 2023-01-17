from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivableMixin(models.Model):
    """
    Mixin with support to active field
    """

    class Meta:
        abstract = True

    active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        null=False,
        blank=False,
    )
