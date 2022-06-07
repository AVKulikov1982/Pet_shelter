from django.shortcuts import render, redirect
from django.views import generic, View
from .models import PetType, PetModel, File
from .forms import AddPetForm, UploadFileForm, UpdatePetForm, PublishedForm
from django.http import HttpResponseBadRequest, HttpResponseForbidden


class CatalogListView(View):

	@staticmethod
	def get(request, type_id):
		pets = PetModel.objects.select_related('file').filter(type_id=type_id)
		return render(request, 'catalog_list_pets.html', context={'pets': pets})


class CatalogDetailView(View):

	@staticmethod
	def get(request, pk):
		pet = PetModel.objects.select_related('file').get(id=pk)
		print(pet.file)
		return render(request, 'catalog_detail_pet.html', context={'pet': pet})


class UpdatePet(View):

	@staticmethod
	def get(request, pk):
		pet = PetModel.objects.get(id=pk)
		pet_form = UpdatePetForm(instance=pet)
		file_form = UploadFileForm()
		return render(request, 'update_pet.html', context={'pet_form': pet_form, 'file_form': file_form, 'pk': pk})

	@staticmethod
	def post(request, pk):
		if request.user.is_authenticated:
			pet = PetModel.objects.get(id=pk)
			pet_form = UpdatePetForm(request.POST)
			file_form = UploadFileForm(request.POST, request.FILES)
			if pet_form.is_valid():
				pet.name = pet_form.cleaned_data.get('name')
				pet.type = pet_form.cleaned_data.get('type')
				pet.age = pet_form.cleaned_data.get('age')
				pet.date_from = pet_form.cleaned_data.get('date_from')
				pet.weight = pet_form.cleaned_data.get('weight')
				pet.growth = pet_form.cleaned_data.get('growth')
				pet.special_signs = pet_form.cleaned_data.get('special_signs')
				pet.published = pet_form.cleaned_data.get('published')
				if file_form.is_valid() and request.FILES.getlist('file'):
					file = request.FILES.getlist('file')[0]
					file_object = File(file=file)
					file_object.save()
					pet.file = file_object
				pet.save()
		else:
			return HttpResponseForbidden('нет прав пользователя')
		return redirect('/')


class AddPet(View):

	@staticmethod
	def get(request):
		pet_form = AddPetForm()
		file_form = UploadFileForm()
		return render(request, 'add_pet.html', context={'pet_form': pet_form, 'file_form': file_form})

	@staticmethod
	def post(request):
		if request.user.is_authenticated:
			pet_form = AddPetForm(request.POST)
			file_form = UploadFileForm(request.POST, request.FILES)
			if pet_form.is_valid():
				name = pet_form.cleaned_data.get('name')
				type = pet_form.cleaned_data.get('type')
				age = pet_form.cleaned_data.get('age')
				date_from = pet_form.cleaned_data.get('date_from')
				weight = pet_form.cleaned_data.get('weight')
				growth = pet_form.cleaned_data.get('growth')
				special_signs = pet_form.cleaned_data.get('special_signs')
				file_object = None
				if file_form.is_valid() and request.FILES.getlist('file'):
					file = request.FILES.getlist('file')[0]
					file_object = File(file=file)
					file_object.save()

				PetModel.objects.create(name=name, type=type, age=age, date_from=date_from, weight=weight,
											  growth=growth, special_signs=special_signs, file=file_object)
				return redirect('/')
		else:
			return HttpResponseForbidden('нет прав пользователя')
		return HttpResponseBadRequest('что-то ввели неправильно')


def catalog(request):
	titles = PetType.objects.values_list('title', flat=True)
	if 'Кошки' not in titles:
		PetType.objects.create(title='Кошки')
	if 'Собаки' not in titles:
		PetType.objects.create(title='Собаки')
	context = PetType.objects.all()
	return render(request, 'catalog_list_types.html', {'context': context})


def unpublished_list(request):
	pets = PetModel.objects.select_related('file').filter(published=False)
	published_form = PublishedForm()
	if request.method == 'POST':
		if request.user.is_superuser:
			if request.POST.getlist('published'):
				for pet in pets:
					pet.published = True
				pets.bulk_update(pets, ['published'])
				return redirect('/')
		else:
			return HttpResponseForbidden('нет прав администратора')
	return render(request, 'unpublished_list.html', context={'pets': pets, 'published_form': published_form})


def unpublished(request, pk):
	data = PetModel.objects.select_related('file').get(id=pk)
	published_form = PublishedForm()
	if request.method == 'POST':
		if request.user.is_superuser:
			if request.POST.getlist('published'):
				pet = PetModel.objects.get(id=pk)
				pet.published = True
				pet.save()
				return redirect('/')
		else:
			return HttpResponseForbidden('нет прав администратора')
	return render(request, 'unpublished.html', context={'pet': data, 'published_form': published_form})