"""library_management_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from library_management_api.settings import DEBUG
# Define swagger api constant
API_VERSION = "v1"
API_VERSION_URL = "api/" + API_VERSION + "/"
API_DESCRIPTION = 'library_management Api Documentation'


schema_view = get_schema_view(
    openapi.Info(
        title="Employee_management API Document",
        default_version=API_VERSION,
        description=API_DESCRIPTION,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION_URL, include(('apps.book.urls', 'book'), namespace='book')),
]

if DEBUG:
    urlpatterns.append(
        path('apidoc/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui')
    )