from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # path("grappelli/", include("grappelli.urls")),
    # path("jet/", include("jet_reboot.urls", "jet_reboot")),
    path('d/', admin.site.urls),
    path('', include('exams.urls')),
    path('schedule/', include('exam_schedule.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)