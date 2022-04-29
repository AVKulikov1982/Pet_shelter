from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import CatalogListView, CatalogDetailView, UpdatePet, AddPet, catalog


urlpatterns = [
	path('catalog/', catalog, name='catalog_list_types'),
	path('catalog/<int:type_id>', CatalogListView.as_view(), name='catalog_list_pets'),
	path('catalog/pet/<int:pk>', CatalogDetailView.as_view(), name='catalog_detail_pet'),
	path('catalog/pet/<int:pk>/update_pet/', UpdatePet.as_view(), name='catalog_detail_pet'),
	path('add_pet', AddPet.as_view(), name='catalog_detail_pet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)