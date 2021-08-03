"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .router import router
from app.clients.views import ClientToken
from app.core.views import RecoverPassword
from app.payments.views import ListenSubscriptionStatus, ApiKey

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API - BoilerPlate React-Django",
        default_version='v1',
        description="This API allows us to keep a diary of our daily drinking",
        terms_of_service="https://google.com",
        contact=openapi.Contact(
            name="Filipe Lopes", email="contato@filipelopes.me", url="https://filipelopes.me"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(router.urls)),
    re_path(r'api/v1/pagarme/listen_subscription_status/(?P<pagarme_subscription_id>[-\w]+)', ListenSubscriptionStatus.as_view()),
    path('api/v1/pagarme/api_key/', ApiKey.as_view()),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/token/client', ClientToken.as_view()),
    path('api/v1/users/recover-password', RecoverPassword.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
