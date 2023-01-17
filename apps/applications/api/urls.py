from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('plans', viewsets.PlanViewSet)
router.register('apps', viewsets.ApplicationViewSet)

app_router = routers.NestedSimpleRouter(parent_router=router, parent_prefix='apps', lookup='app')
app_router.register(r'subscriptions', viewsets.SubscriptionHistoryViewSet, basename='app-subscriptions')

urlpatterns = router.urls
urlpatterns += app_router.urls
