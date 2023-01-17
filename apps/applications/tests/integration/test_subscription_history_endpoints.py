from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from .. import factories


class PlanCreationEndpointTestCase(TestCase):
    def setUp(self) -> None:
        self.app = factories.ApplicationFactory()
        self.endpoint = reverse_lazy('application:app-subscriptions-list', kwargs={'app_id': str(self.app.pk)})
        self.user = factories.UserFactory()

    def test_creation_restriction(self):
        """ Tests whether POST endpoint as NOT supported. """
        response = self.client.post(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_supported(self):
        """ Tests whether POST endpoint as NOT supported. """
        self.client.force_login(self.user)
        response = self.client.post(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestSubscriptionHistoryListEndpoint(TestCase):
    def setUp(self) -> None:
        self.app = factories.ApplicationFactory()
        self.endpoint = reverse_lazy('application:app-subscriptions-list', kwargs={'app_id': str(self.app.pk)})
        self.user = factories.UserFactory()

        self.items = factories.SubscriptionHistoryFactory.create_batch(10, app=self.app)
        self.items_to_ignore = factories.SubscriptionHistoryFactory.create_batch(10)

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

        not_pks = [i['id'] for i in result['results']]
        for item in self.items_to_ignore:
            self.assertNotIn(str(item.pk), not_pks)


class TestSubscriptionHistoryItemEndpoint(TestCase):
    def setUp(self) -> None:
        self.app = factories.ApplicationFactory.create()
        self.item = factories.SubscriptionHistoryFactory.create(app=self.app)
        self.endpoint = reverse_lazy('application:app-subscriptions-detail', kwargs={
            'app_id': str(self.app.pk),
            'id': str(self.item.pk),
        })
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

        self.assertEqual(result['old_plan_name'], self.item.old_plan_name)
        self.assertEqual(result['old_price'], self.item.old_price)
        self.assertEqual(result['current_plan_name'], self.item.current_plan_name)
        self.assertEqual(result['action_type'], str(self.item.action_type))

        self.assertIn('created_at', result)


class TestSubscriptionHistoryEditionEndpoint(TestCase):
    def setUp(self) -> None:
        self.app = factories.ApplicationFactory.create()
        self.item = factories.SubscriptionHistoryFactory.create(app=self.app)
        self.endpoint = reverse_lazy('application:app-subscriptions-detail', kwargs={
            'app_id': str(self.app.pk),
            'id': str(self.item.pk),
        })
        self.user = factories.UserFactory()

    def test_item_retrieval_restriction(self):
        """ Tests whether item endpoint is restricted to authenticated users. """
        response = self.client.put(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_supported(self):
        """ Tests whether PATCH endpoint as NOT supported. """
        self.client.force_login(self.user)
        response = self.client.put(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestSubscriptionHistoryDeletionEndpoint(TestCase):
    def setUp(self) -> None:
        self.app = factories.ApplicationFactory.create()
        self.item = factories.SubscriptionHistoryFactory.create(app=self.app)
        self.endpoint = reverse_lazy('application:app-subscriptions-detail', kwargs={
            'app_id': str(self.app.pk),
            'id': str(self.item.pk),
        })
        self.user = factories.UserFactory()

    def test_item_deletion_restriction(self):
        """ Tests whether item DELETE endpoint is restricted to authenticated users. """
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_item_deletion(self):
        """ Tests item DELETE endpoint. """
        self.client.force_login(self.user)
        response = self.client.delete(self.endpoint, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
