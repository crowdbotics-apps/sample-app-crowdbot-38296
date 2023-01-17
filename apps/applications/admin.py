from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.applications import models, forms


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    form = forms.PlanForm
    ordering = ['price', ]
    search_fields = ('pk', 'name',)
    list_display = ('name', 'price', 'active')


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = forms.ApplicationForm
    search_fields = ('pk', 'name', 'category__name', 'category_id')
    list_display = ('name', 'user', 'active', 'price', 'created_at')
    list_filter = ('user',)

    def price(self, obj):
        return obj.plan.price if obj.plan else 'Free'

    price.name = _('Price')


@admin.register(models.SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    search_fields = ('pk', 'current_plan_name', 'old_plan_name', 'action_type', 'created_at')
    list_display = ('app', 'action_type', 'track_plan_name', 'track_plan_price', 'created_at')
    list_filter = ('app',)

    readonly_fields = (
        'pk',
        'app',
        'action_type',
        'old_plan_name',
        'current_plan_name',
        'old_price',
        'current_price',
        'created_at',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
