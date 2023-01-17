from decimal import Decimal

import pytest

from . import factories

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
@pytest.fixture
def plan():
    return factories.PlanFactory()


@pytest.mark.django_db
@pytest.fixture
def free_plan():
    plan = factories.PlanFactory()
    plan.price = Decimal(0)
    plan.save()
    return plan


@pytest.mark.django_db
@pytest.fixture
def application_no_plan():
    app = factories.ApplicationFactory()
    app.plan = None
    app.save()
    return app


@pytest.mark.django_db
@pytest.fixture
def application():
    return factories.ApplicationFactory()
