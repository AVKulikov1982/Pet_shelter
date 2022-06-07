import datetime
import os
import random

from django.test import TestCase
from django.urls import reverse
from ..models import PetType, PetModel
from pet_shelter_project.app_users.models import Avatar, Profile
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
		Profile.objects.create(
			user=user,
			phone=22222222222,
		)

		for pet_index in range(1, number_of_pets + 1):
			if pet_index == 1:
				PetType.object.create(title='cats')
			elif pet_index == 2:
				PetType.object.create(title='dogs')
			if pet_index % 2 == 0:
				PetModel.objects.create(
					name=f'pet - {pet_index}',
					type=1,
					age=random.randint(1, 4),
					date_from = datetime.date.today().strftime("%d-%m-%Y"),
					weight = random.randint(1, 3),
					growth = random.randint(1, 3),
					special_signs = f'test_description {pet_index}'
				)

	def test_can_add_pet(self):
		url = reverse('add_pet')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'app_pets/add_pet.html')

		user = User.objects.all()[0]
		self.client.login(username='test_user', password='test_user')
		permission = Permission.objects.get(name='Can add pet')
		user.user_permissions.add(permission)
		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '01-01-2022',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(PetModel.objects.last().name, 'test_name')
		self.assertEqual(PetModel.objects.last().type, 1)
		self.assertEqual(PetModel.objects.last().age, 1)
		self.assertEqual(PetModel.objects.last().date_from, '01-01-2022')
		self.assertEqual(PetModel.objects.last().weight, 1)
		self.assertEqual(PetModel.objects.last().growth, 1)
		self.assertEqual(PetModel.objects.last().special_signs, 'test_description')

	def test_can_not_add_pet(self):
		url = reverse('add_pet')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'app_pets/add_pet.html')

		response = self.client.post(url, {
			'name': 'test_name',
			'type': 1,
			'age': 1,
			'date_from': '01-01-2022',
			'weight': 1,
			'growth': 1,
			'special_signs': 'test_description'
		})
		self.assertEqual(response.status_code, 403)

	def test_pets_list(self):
		url = reverse('list_pets')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'app_pets/catalog_list_pets.html')
		self.assertTrue(len(response.context['list_pets']) == number_of_pets)

	def test_pet_detail(self):
		number = 3
		url = reverse('detail_pet', args=[number])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'app_pets/catalog_detail_pet.html')
		self.assertTrue(str(number) in response.context['pet'].name)

	def test_update_pet(self):
		pass

	def test_can_not_update_pet(self):
		pass

	def test_delete_pet(self):
		pass

	def test_can_not_delete_pet(self):
		pass