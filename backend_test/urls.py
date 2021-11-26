"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from .utils.healthz import healthz

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api_urls = [
    path(
        "v1/",
        include(
            [
                path("", include("apps.menu.api.urls"), name="menu"),
                path("", include("apps.location.api.urls"), name="location"),
            ]
        ),
    ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("user/", include(("apps.profile_user.urls", "profile"), namespace="profile")),
    path("menu/", include(("apps.menu.urls", "menu"), namespace="menu")),
    path(
        "location/", include(("apps.location.urls", "location"), namespace="location")
    ),
    path("api/", include((api_urls, "api"), namespace="api")),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    # User management
    path("accounts/", include("allauth.urls")),
]
