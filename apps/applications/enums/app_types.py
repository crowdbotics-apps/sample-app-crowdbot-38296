from django.db.models import TextChoices

from ..constants import APP_TYPE_WEB, APP_TYPE_MOBILE


class AppType(TextChoices):
    WEB = APP_TYPE_WEB, 'Web'
    MOBILE = APP_TYPE_MOBILE, 'Mobile'
