"""explonary URL Configuration

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
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Explonary API",
      default_version='v1',
      description="Make soccer great again!",
      terms_of_service="https://explonary.com/terms/",
      contact=openapi.Contact(email="info@explonary.com"),
      license=openapi.License(name="BSD License"),
      url="https://explonary.com/api"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    path(r'user/', include('user.urls')),
    path(r'content/', include('content.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
