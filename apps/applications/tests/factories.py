import factory
from django.conf import settings
from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from apps.applications import enums
from apps.applications import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('first_name', 'last_name', 'email')

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = Faker("user_name")
    is_active = True
    is_superuser = False


class PlanFactory(DjangoModelFactory):
    class Meta:
        model = models.Plan
        django_get_or_create = ('name', 'description', 'price')

    name = Faker("name")
    description = Faker("paragraph")
    price = Faker("pydecimal", positive=True, left_digits=3, right_digits=2)


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = models.Application
        django_get_or_create = ('name', 'type', 'framework',)

    name = Faker("name")
    description = Faker("paragraph")
    domain_name = Faker('name')
    screenshot = Faker('url')

    type = fuzzy.FuzzyChoice(enums.AppType.choices, getter=lambda c: c[0])
    framework = fuzzy.FuzzyChoice(enums.AppFramework.choices, getter=lambda c: c[0])

    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)


class SubscriptionHistoryFactory(DjangoModelFactory):
    class Meta:
        model = models.SubscriptionHistory

    current_plan_name = Faker("name")
    current_price = Faker("pydecimal", positive=True, left_digits=3, right_digits=2)

    old_plan_name = None
    old_price = None

    action_type = fuzzy.FuzzyChoice(enums.PlanActionType.choices, getter=lambda c: c[0])

    app = factory.SubFactory(ApplicationFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs.update({'ignore_validation': True})
        return super()._create(model_class, *args, **kwargs)

