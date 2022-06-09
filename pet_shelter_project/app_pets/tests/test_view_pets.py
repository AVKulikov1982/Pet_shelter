import datetime
import os
import random

from django.test import TestCase
from django.urls import reverse
from ..models import PetType, PetModel
from app_users.models import Avatar, Profile
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login

number_of_pets = 10


class PetsViewsTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		user = User.objects.create_user(
			username='test_user',
			email='test@test.ru',
			password='test_user'
		)
		Profile.objects.create(user=user)
		PetType.objects.create(title='cats')
		PetType.objects.create(title='dogs')
		for pet_index in range(1, number_of_pets + 1):
			if pet_index % 2 == 0:
				pet_type = PetType.objects.get(title='cats')
			else:
				pet_type = PetType.objects.get(title='dogs')
			PetModel.objects.create(
				name=f'pet - {pet_index}',
				type=pet_type,
				age=random.randint(1, 4),
				date_from=datetime.date.today().strftime("%Y-%m-%d"),
				weight=random.randint(1, 3),
				growth=random.randint(1, 3),
				special_signs=f'test_description {pet_index}'
			)

	def test_can_add_pet(self):
		url = reverse('add_pet')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'add_pet.html')
		self.client.login(username='test_user', password='test_user')
		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '2022-01-01',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(PetModel.objects.last().name, 'test_name')
		self.assertEqual(PetModel.objects.last().type.id, 1)
		self.assertEqual(PetModel.objects.last().age, 1)
		self.assertEqual(PetModel.objects.last().date_from.strftime("%Y-%m-%d"), '2022-01-01')
		self.assertEqual(PetModel.objects.last().weight, 1)
		self.assertEqual(PetModel.objects.last().growth, 1)
		self.assertEqual(PetModel.objects.last().special_signs, 'test_description')

	def test_can_not_add_pet(self):
		url = reverse('add_pet')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'add_pet.html')
		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '2022-01-01',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		self.assertEqual(response.status_code, 403)

	def test_pets_list(self):
		url = reverse('list_pets', args=[1])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'catalog_list_pets.html')
		self.assertTrue(len(response.context['pets']) == number_of_pets / 2)

	def test_pet_detail(self):
		number = 3
		url = reverse('detail_pet', args=[number])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'catalog_detail_pet.html')
		self.assertTrue(str(number) in response.context['pet'].name)

	def test_can_update_pet(self):
		url = reverse('update_pet', args=[2])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update_pet.html')
		pet = PetModel.objects.get(id=2)
		self.client.login(username='test_user', password='test_user')
		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '2022-01-01',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		pet.refresh_from_db()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(pet.name, 'test_name')
		self.assertEqual(pet.type.id, 1)
		self.assertEqual(pet.age, 1)
		self.assertEqual(pet.date_from.strftime("%Y-%m-%d"), '2022-01-01')
		self.assertEqual(pet.weight, 1)
		self.assertEqual(pet.growth, 1)
		self.assertEqual(pet.special_signs, 'test_description')

	def test_can_not_update_pet(self):
		url = reverse('update_pet', args=[4])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update_pet.html')
		pet = PetModel.objects.get(id=4)
		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '2022-01-01',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		pet.refresh_from_db()
		self.assertEqual(response.status_code, 403)
		self.assertFalse(pet.name == 'test_name')

	def test_delete_pet(self):
		url = reverse('delete_pet', args=[7])
		User.objects.create_superuser('s_user', 's_user@test.ru', 's_user_password')
		self.client.login(username='s_user', password='s_user_password')
		response = self.client.get(url)
		pets = PetModel.objects.all().values_list('id', flat=True)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(number_of_pets - len(pets), 1)
		self.assertTrue(7 not in pets)

	def test_can_not_delete_pet(self):
		url = reverse('delete_pet', args=[6])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)
