from django.contrib import admin
from .models import PetType, PetModel


@admin.register(PetType)
class PetModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'title']


@admin.register(PetModel)
class PetModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'age', 'special_signs', 'published']
	list_filter = ['name', 'special_signs', 'published']
	search_fields = ['name', 'special_signs']