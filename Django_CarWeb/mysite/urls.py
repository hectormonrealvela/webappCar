from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from Document.models import Document









urlpatterns = [
                    url('', include('Document.urls')),
                    url(r'^admin/', (admin.site.urls)),




]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
