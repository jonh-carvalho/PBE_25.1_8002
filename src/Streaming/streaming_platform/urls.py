from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
   openapi.Info(
      title="API de Produtos",
      default_version='v1',
      description="API para gerenciamento de produtos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@empresa.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content_app.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]