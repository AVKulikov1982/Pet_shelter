from django.shortcuts import render, redirect
from django.views import generic, View
from .models import PetType, PetModel
from .forms import AddPetForm, UpdatePetForm


class CatalogListView(View):

	@staticmethod
	def get(request, type_id):
		pets = PetModel.objects.filter(type=type_id)
		return render(request, 'catalog_list_pets.html', context={'pets': pets})


class CatalogDetailView(generic.DetailView):
	model = PetModel
	template_name = 'catalog_detail_pet.html'


class UpdatePet(View):

	@staticmethod
	def get(request, pk):
		pet = PetModel.objects.get(id=pk)
		pet_form = UpdatePetForm(instance=pet)
		return render(request, 'update_pet.html', context={'pet_form': pet_form, 'pk': pk})

	@staticmethod
	def post(request, pk):
		pet = PetModel.objects.get(id=pk)
		pet_form = UpdatePetForm(request.POST)
		if pet_form.is_valid():
			pet.name = pet_form.cleaned_data.get('name')
			pet.type = pet_form.cleaned_data.get('type')
			pet.age = pet_form.cleaned_data.get('age')
			pet.date_from = pet_form.cleaned_data.get('date_from')
			pet.weight = pet_form.cleaned_data.get('weight')
			pet.growth = pet_form.cleaned_data.get('growth')
			pet.special_signs = pet_form.cleaned_data.get('special_signs')
			pet.published = pet_form.cleaned_data.get('published')
			pet.save()
		return redirect('/')


class AddPet(View):

	@staticmethod
	def get(request):
		pet_form = AddPetForm()
		return render(request, 'add_pet.html', context={'pet_form': pet_form})

	@staticmethod
	def post(request):
		pet_form = AddPetForm(request.POST)

		if pet_form.is_valid():
			name = pet_form.cleaned_data.get('name')
			type = pet_form.cleaned_data.get('type')
			age = pet_form.cleaned_data.get('age')
			date_from = pet_form.cleaned_data.get('date_from')
			weight = pet_form.cleaned_data.get('weight')
			growth = pet_form.cleaned_data.get('growth')
			special_signs = pet_form.cleaned_data.get('special_signs')
			pet = PetModel.objects.create(name=name, type=type, age=age, date_from=date_from, weight=weight,
										 growth=growth, special_signs=special_signs)
			pet.save()
		return redirect('/')



def catalog(request):
	titles = PetType.objects.values_list('title', flat=True)
	if 'Кошки' not in titles:
		PetType.objects.create(title='Кошки')
	if 'Собаки' not in titles:
		PetType.objects.create(title='Собаки')
	context = PetType.objects.all()
	return render(request, 'catalog_list_types.html', {'context': context})