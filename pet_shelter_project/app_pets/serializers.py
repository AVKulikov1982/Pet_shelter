from .models import PetModel, File
from rest_framework import serializers


class PetSerializer(serializers.ModelSerializer):
	"""Сериализатор модели Животное"""
	class Meta:
		model = PetModel
		fields = ['id', 'name', 'type', 'age', 'date_from', 'weight', 'growth', 'special_signs', 'file']
