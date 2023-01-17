from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from .. import factories
from ...api import serializers
from ...models import Plan


def create_plan_data() -> dict:
    plan = factories.PlanFactory.build()
    data = serializers.PlanSerializer(instance=plan).data
    data.pop('id')
    data.pop('created_at')
    data.pop('updated_at')
    return data


def get_plan_data(instance: Plan) -> dict:
    return serializers.PlanSerializer(instance=instance).data


class TestPlanCreationEndpoint(TestCase):
    def setUp(self) -> None:
        self.endpoint = reverse_lazy('application:plan-list')
        self.user = factories.UserFactory()

    def test_creation_restriction(self):
        """ Tests whether POST endpoint is restricted to authenticated users. """
        response = self.client.post(self.endpoint, data=create_plan_data(),  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creation(self):
        """ Tests POST endpoint """
        self.client.force_login(self.user)

        data = create_plan_data()
        response = self.client.post(self.endpoint, data=data,  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.json()

        self.assertEqual(Plan.objects.filter(pk=result['id']).exists(), True)
        self.assertEqual(result['name'], data['name'])
        self.assertEqual(result['price'], data['price'])
        self.assertEqual(result['active'], data['active'])
        self.assertEqual(result['description'], data['description'])
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)


class TestPlanListEndpoint(TestCase):
    def setUp(self) -> None:
        self.endpoint = reverse_lazy('application:plan-list')
        self.user = factories.UserFactory()

        self.items = factories.PlanFactory.create_batch(10)

    def test_list_retrieval_restriction(self):
        """ Tests whether list endpoint is restricted to authenticated users. """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_retrieval(self):
        """ Tests output of list endpoint. """
        self.client.force_login(self.user)
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertEqual(result['count'], len(self.items))

        pks = [i['id'] for i in result['results']]
        for item in self.items:
            self.assertIn(str(item.pk), pks)


class TestPlanItemEndpoint(TestCase):
    def setUp(self) -> None:
        self.item = factories.PlanFactory.create()
        self.endpoint = reverse_lazy('application:plan-detail', kwargs={'id': str(self.item.pk)})
        self.user = factories.UserFactory()

    def test_item_retrieval_restriction(self):
        """ Tests whether item endpoint is restricted to authenticated users. """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_item_retrieval(self):
        """ Tests output of item endpoint. """
        self.client.force_login(self.user)
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertEqual(result['id'], str(self.item.pk))
        self.assertEqual(result['name'], self.item.name)
        self.assertEqual(result['price'], str(self.item.price))
        self.assertEqual(result['active'], self.item.active)
        self.assertEqual(result['description'], self.item.description)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)


class TestPlanEditionEndpoint(TestCase):
    def setUp(self) -> None:
        self.item = factories.PlanFactory.create()
        self.endpoint = reverse_lazy('application:plan-detail', kwargs={'id': str(self.item.pk)})
        self.user = factories.UserFactory()

    def test_item_edition_restriction(self):
        """ Tests whether item EDITION endpoint is restricted to authenticated users. """
        data = get_plan_data(self.item)
        response = self.client.put(self.endpoint, data=data,  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.endpoint, data=data,  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update(self):
        """ Tests item EDITION endpoint. """
        data = get_plan_data(self.item)

        name = self.item.name + '-edited'
        active = not self.item.active
        desc = self.item.description + ' -- changed'

        data.update({'name': name, 'active': active, 'description': desc})

        self.client.force_login(self.user)
        response = self.client.put(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertEqual(result['id'], str(self.item.pk))
        self.assertEqual(result['name'], name)
        self.assertEqual(result['price'], str(self.item.price))
        self.assertEqual(result['active'], active)
        self.assertEqual(result['description'], desc)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)

    def test_partial_update(self):
        """ Tests item EDITION endpoint. """
        data = {
            'name': self.item.name + '--edited',
            'active': not self.item.active,
            'description': self.item.description + '-- edited',
            'price': str(round(self.item.price ** 2, 2))
        }

        self.client.force_login(self.user)
        edited_data = dict()
        for k, v in data.items():
            self.item.refresh_from_db()
            data_to_send = {k: v}

            response = self.client.patch(self.endpoint, data=data_to_send, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            result = response.json()
            edited_data.update(result)

        self.assertEqual(data['name'], edited_data['name'])
        self.assertEqual(data['description'], edited_data['description'])
        self.assertEqual(data['active'], edited_data['active'])
        self.assertEqual(data['price'], edited_data['price'])


class TestPlanDeletionEndpoint(TestCase):
    def setUp(self) -> None:
        self.item = factories.PlanFactory.create()
        self.endpoint = reverse_lazy('application:plan-detail', kwargs={'id': str(self.item.pk)})
        self.user = factories.UserFactory()

    def test_item_deletion_restriction(self):
        """ Tests whether item DELETE endpoint is restricted to authenticated users. """
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_item_deletion(self):
        """ Tests item DELETE endpoint. """
        queryset = Plan.objects.get_queryset()

        self.assertEqual(queryset.filter(pk=self.item.pk).exists(), True)

        self.client.force_login(self.user)
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(queryset.filter(pk=self.item.pk).exists(), False)
