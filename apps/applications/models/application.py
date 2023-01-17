from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins, track_data
from ..enums import AppType, AppFramework


@track_data('plan_id')
class Application(mixins.UUIDPkMixin,
                  mixins.ActivableMixin,
                  mixins.DateTimeManagementMixin,
                  mixins.EntityMixin,
                  models.Model):
    """
    An app the user has created in our platform. Includes metadata about the app such
    as name and description.
    """

    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')
        ordering = ['name']

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
        null=False,
        blank=False,
        help_text=_('Provide a name for the app'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
    )

    type = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name=_('app type'),
        choices=AppType.choices,
    )

    framework = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_('framework'),
        choices=AppFramework.choices,
    )

    domain_name = models.CharField(
        max_length=50,
        verbose_name=_('domain name'),
        null=True,
        blank=True,
        help_text=_('Provide the name of you domain'),
    )

    screenshot = models.URLField(
        verbose_name=_('screenshot'),
        null=True,
        blank=True,
        help_text=_('Provide a URL with an image that shows your application'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=False,
        blank=False,
        on_delete=models.RESTRICT,
    )

    plan = models.ForeignKey(
        "applications.Plan",
        null=True,
        blank=True,
        verbose_name=_('plan'),
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    @property
    def free(self) -> bool:
        if not self.plan_id:
            return True
        return not self.plan.price

    def __str__(self):
        return self.name
