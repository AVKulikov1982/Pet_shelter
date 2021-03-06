from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import CatalogListView, CatalogDetailView, UpdatePet, AddPet, catalog, unpublished_list, unpublished, delete
from .api import PetList
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/pets', PetList)

urlpatterns = [
	path('catalog/', catalog, name='catalog_list_types'),
	path('catalog/unpublished/', unpublished_list, name='unpublished_list'),
	path('catalog/unpublished/pet/<int:pk>', unpublished, name='unpublished_detail'),
	path('catalog/<int:type_id>', CatalogListView.as_view(), name='list_pets'),
	path('catalog/pet/<int:pk>', CatalogDetailView.as_view(), name='detail_pet'),
	path('catalog/pet/<int:pk>/update_pet/', UpdatePet.as_view(), name='update_pet'),
	path('add_pet', AddPet.as_view(), name='add_pet'),
	path('catalog/pet/<int:pk>/delete', delete, name='delete_pet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls