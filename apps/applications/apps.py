from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApplicationConfig(AppConfig):
    name = 'apps.applications'
    label = 'applications'
    verbose_name = _('Crowdbotics applications')

    # noinspection PyUnresolvedReferences
    def ready(self):
        from . import signals
