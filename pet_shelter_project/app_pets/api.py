from .models import PetModel
from rest_framework.viewsets import ModelViewSet
from .serializers import PetSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


class PetList(ModelViewSet):
	serializer_class = PetSerializer
	queryset = PetModel.objects.select_related('file')
	permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
									'retrieve': [IsAuthenticated],
									'update': [IsAuthenticated],
									'destroy': [IsAdminUser],
									}
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	ordering_fields = ['name', 'growth', 'age']

	def get_permissions(self):
		try:
			# return permission_classes depending on `action`
			return [permission() for permission in self.permission_classes_by_action[self.action]]
		except KeyError:
			# action is not set return default permission_classes
			return [permission() for permission in self.permission_classes]
