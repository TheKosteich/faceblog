from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from faceblog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',  include('blog.urls', namespace='blog')),
]


# Django urls setting for development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
