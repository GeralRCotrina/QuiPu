from django.contrib import admin
from django.urls import path, re_path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   	path('admin/', admin.site.urls),
    re_path(r'^',include('apps.gestion.urls')),
    re_path(r'^',include('apps.peti.urls')),
    re_path(r'^',include('apps.esta.urls')),
    re_path(r'^',include('apps.requ.urls')),
    re_path(r'^',include('apps.inci.urls')),
    re_path(r'^',include('apps.ries.urls')),
    re_path(r'^',include('apps.task.urls')),
    re_path(r'^',include('apps.duda.urls')),
    re_path(r'^',include('apps.gant.urls')),
    re_path(r'^',include('apps.peer.urls')),
    re_path(r'^',include('apps.esti.urls')),
    re_path(r'^',include('apps.repo.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  