from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from qysnart import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainwebsite.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#Step 6 : Setup to access static file in debug mode
    urlpatterns += staticfiles_urlpatterns()