from django.urls import path, include
from .views import home, results
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', home),
    path('results/', results, name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)