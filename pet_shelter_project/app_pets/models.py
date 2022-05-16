from django.db import models
from django.utils.translation import gettext_lazy as _


class PetType(models.Model):

	title = models.CharField(max_length=30, verbose_name=_('тип животного'))

	def get_object(self):
		view_object = super(PetType, self).get_object()
		print(view_object)

	def __str__(self):
		return self.title

class PetModel(models.Model):

	name = models.CharField(max_length=30, db_index=True, verbose_name=_('кличка животного'))
	type = models.ForeignKey(PetType, on_delete=models.CASCADE, verbose_name=_('тип животного'), default=None, null=True)
	age = models.PositiveIntegerField(verbose_name=_('возраст животного'))
	date_from = models.DateField(verbose_name=_('дата прибытия в приют'))
	weight = models.PositiveIntegerField(verbose_name=_('вес животного'))
	growth = models.PositiveIntegerField(verbose_name=_('рост животного'))
	special_signs = models.CharField(max_length=200, verbose_name=_('особые приметы животного'))
	published = models.BooleanField(default=False, verbose_name=_('опубликовать'))

	def __str__(self):
		return self.name
