from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from .yasg import urlpatterns as yasg


api_version = 'api/v1'


urlpatterns = [
    path('admin/', admin.site.urls),

    path(f'{api_version}/auth/', include('authenticate.urls')),
    path(f'{api_version}/courses/', include('courses.urls')),
] + yasg

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
