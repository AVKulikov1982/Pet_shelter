from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import main, contacts


urlpatterns = [
	path('', main, name='home'),
	path('contacts/', contacts, name='contacts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)