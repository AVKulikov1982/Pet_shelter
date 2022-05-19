from django import forms
from django.utils.translation import gettext as _
from .models import PetModel


class AddPetForm(forms.ModelForm):
	class Meta:
		model = PetModel
		fields = ['name', 'type', 'age', 'date_from', 'weight', 'growth', 'special_signs']


class UploadFileForm(forms.Form):
	file = forms.FileField(required=False)


class UpdatePetForm(forms.ModelForm):
	class Meta:
		model = PetModel
		fields = ['name', 'type', 'age', 'date_from', 'weight', 'growth', 'special_signs', 'published']


class PublishedForm(forms.Form):
	published = forms.BooleanField(required=False, widget=forms.CheckboxInput)