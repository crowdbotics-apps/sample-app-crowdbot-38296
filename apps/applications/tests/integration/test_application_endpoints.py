from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from apps.users.api.serializers import SimpleUserSerializer
from apps.users.models import User
from .. import factories
from ...api import serializers
from ...models import Application, Plan


def create_application_data() -> dict:
    plan = factories.ApplicationFactory.build()
    data = serializers.ApplicationSerializer(instance=plan).data
    data.pop('id')
    data.pop('user')
    data.pop('plan')
    data.pop('created_at')
    data.pop('updated_at')
    return data


def get_application_data(instance: Application) -> dict:
    return serializers.ApplicationSerializer(instance=instance).data


def get_plan_data(instance: Plan) -> dict:
    return serializers.SimplePlanSerializer(instance=instance).data


def get_user_data(instance: User) -> dict:
    return SimpleUserSerializer(instance=instance).data


class TestAppCreationEndpoint(TestCase):
    def setUp(self) -> None:
        self.endpoint = reverse_lazy('application:application-list')
        self.user = factories.UserFactory()

    def test_creation_restriction(self):
        """ Tests whether POST endpoint is restricted to authenticated users. """
        response = self.client.post(self.endpoint, data=create_application_data(), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creation(self):
        """ Tests POST endpoint """
        self.client.force_login(self.user)

        data = create_application_data()
        response = self.client.post(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.json()

        self.assertEqual(Application.objects.filter(pk=result['id']).exists(), True)

        item = Application.objects.get(pk=result['id'])

        self.assertEqual(result['name'], item.name)
        self.assertEqual(result['description'], item.description)
        self.assertEqual(result['active'], item.active)
        self.assertEqual(result['type'], str(item.type))
        self.assertEqual(result['framework'], str(item.framework))
        self.assertEqual(result['domain_name'], item.domain_name)
        self.assertEqual(result['screenshot'], item.screenshot)

        self.assertEqual(result['user'], get_user_data(self.user))  # logged user
        self.assertEqual(result['plan'], get_plan_data(item.plan))

        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)


class TestAppListEndpoint(TestCase):
    def setUp(self) -> None:
        self.endpoint = reverse_lazy('application:application-list')
        self.user = factories.UserFactory()

        self.items = factories.ApplicationFactory.create_batch(10, user=self.user)

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


class TestAppItemEndpoint(TestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.item = factories.ApplicationFactory.create(user=self.user)
        self.endpoint = reverse_lazy('application:application-detail', kwargs={'id': str(self.item.pk)})

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
        self.assertEqual(result['description'], self.item.description)
        self.assertEqual(result['active'], self.item.active)
        self.assertEqual(result['type'], str(self.item.type))
        self.assertEqual(result['framework'], str(self.item.framework))
        self.assertEqual(result['domain_name'], self.item.domain_name)
        self.assertEqual(result['screenshot'], self.item.screenshot)

        self.assertEqual(result['user'], get_user_data(self.user))  # logged user
        self.assertEqual(result['plan'], get_plan_data(self.item.plan))

        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)


class TestAppEditionEndpoint(TestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.item = factories.ApplicationFactory.create(user=self.user)
        self.endpoint = reverse_lazy('application:application-detail', kwargs={'id': str(self.item.pk)})

    def test_item_edition_restriction(self):
        """ Tests whether item EDITION endpoint is restricted to authenticated users. """
        data = get_plan_data(self.item)
        response = self.client.put(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update(self):
        """ Tests item EDITION endpoint. """
        data = get_application_data(self.item)

        name = self.item.name + '-edited'
        active = not self.item.active
        desc = self.item.description + ' -- changed'
        plan = get_plan_data(factories.PlanFactory())

        data.update({'name': name, 'active': active, 'description': desc, 'plan': plan})

        self.client.force_login(self.user)
        response = self.client.put(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertEqual(result['id'], str(self.item.pk))
        self.assertEqual(result['name'], name)
        self.assertEqual(result['active'], active)
        self.assertEqual(result['description'], desc)

        self.assertEqual(result['plan'], plan)

    def test_partial_update(self):
        """ Tests item EDITION endpoint when plan is added. """
        data = {
            'name': self.item.name + '--edited',
            'active': not self.item.active,
            'description': self.item.description + '-- edited',
            'plan': get_plan_data(factories.PlanFactory())
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

        self.assertEqual(edited_data['plan'], edited_data['plan'])

    def test_user_edition_not_supported(self):
        data = {
            'user': get_user_data(factories.UserFactory())
        }

        self.assertNotEqual(str(self.user.pk), data['user']['id'])

        self.client.force_login(self.user)
        response = self.client.patch(self.endpoint, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertNotEqual(result['user']['id'], data['user']['id'])
        self.assertEqual(result['user']['id'], str(self.user.pk))


class TestAppDeletionEndpoint(TestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.item = factories.ApplicationFactory.create(user=self.user)
        self.endpoint = reverse_lazy('application:application-detail', kwargs={'id': str(self.item.pk)})

    def test_item_deletion_restriction(self):
        """ Tests whether item DELETE endpoint is restricted to authenticated users. """
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_item_deletion(self):
        """ Tests item DELETE endpoint. """
        queryset = Application.objects.get_queryset()

        self.assertEqual(queryset.filter(pk=self.item.pk).exists(), True)

        self.client.force_login(self.user)
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(queryset.filter(pk=self.item.pk).exists(), False)
