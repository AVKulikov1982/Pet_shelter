from .models import PetModel
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from .serializers import PetSerializer


class PetList(viewsets.ModelViewSet):
	serializer_class = PetSerializer
	queryset = PetModel.objects.select_related('file')
