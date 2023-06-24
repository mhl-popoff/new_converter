from django.urls import path, re_path
from .views import home, results
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path('', home),
    path('results/', results, name='results'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^results/(?P<path>.*)$', serve, {'document_root': settings.RESULTS_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)