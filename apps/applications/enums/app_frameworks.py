from django.db.models import TextChoices

from ..constants import APP_FRAMEWORK_DJANGO, APP_FRAMEWORK_REACT_NATIVE


class AppFramework(TextChoices):
    DJANGO = APP_FRAMEWORK_DJANGO, 'Django'
    REACT_NATIVE = APP_FRAMEWORK_REACT_NATIVE, 'React Native'
