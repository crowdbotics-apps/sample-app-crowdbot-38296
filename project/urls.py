"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView

admin.site.site_header = "Sample App - Crowdbotic"
admin.site.site_title = "Sample App - Crowdbotic Admin Portal"
admin.site.index_title = "Sample App - Crowdbotic Admin"

admin_urls = [
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path("admin/", admin.site.urls),
]

account_urls = [
    path("accounts/", include("allauth.urls"))
]

module_urls = [
    path("modules/", include("apps.modules.urls"))
]

schema_url_patterns = [
    path('v1/', include(('apps.applications.api.urls', 'applications'), namespace='application')),
    # path('v1/auth/', include(('rest_framework.urls', 'auth'), namespace='rest_framework')),
    path('v1/auth/', include(('dj_rest_auth.urls', 'auth'), namespace='auth')),
    path(
        'v1/auth/registrations/',
        include(('dj_rest_auth.registration.urls', 'auth-registration'), namespace='auth-registration')
    ),
]

util_urls = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('health/', include('health_check.urls')),
]

urlpatterns = admin_urls + account_urls + module_urls + schema_url_patterns + util_urls

# swagger
urlpatterns += [
    path("api-docs/schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    path("api-docs/", SpectacularSwaggerView.as_view(url_name='schema'), name="api_docs")
]

# ============================ STATIC CONFIG ================================ #
urlpatterns += staticfiles_urlpatterns()
