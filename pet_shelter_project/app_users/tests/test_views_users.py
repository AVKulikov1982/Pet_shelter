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

class UsersViewsTest(TestCase):
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


	def test_login(self):
		url = reverse('login')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/login.html')

	def test_logout(self):
		url = reverse('logout')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/logout.html')

	def test_profile(self):
		url = reverse('profile')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/profile.html')

	def test_profile_update_first_name(self):
		url = reverse('profile_update', args=[1])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/profile_update.html')

		user = User.objects.all()[0]
		self.client.login(username='test_user', password='test_user')
		test_phone = 11111111111
		response = self.client.post(url, {
			'username': 'test_username',
			'first_name': 'test_first_name',
			'last_name': 'test_last_name',
			'email': 'test@test.ru',
			'phone': test_phone,
			'date_of_birth': '1982-06-01',
			'new_pass1': 'test_pass',
			'new_pass2': 'test_pass'
		})
		user.refresh_from_db()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(user.username, 'test_username')
		self.assertEqual(user.first_name, 'test_first_name')
		self.assertEqual(user.last_name, 'test_last_name')
		self.assertEqual(user.email, 'test@test.ru')
		self.assertEqual(Profile.objects.get(user=user).phone, test_phone)
		self.assertEqual(Profile.objects.get(user=user).date_of_birth.strftime('%Y-%m-%d'), '1982-06-01')
		self.assertTrue(self.client.login(username='test_username', password='test_pass'))

	def test_can_register(self):
		url = reverse('registration')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/registration.html')

		response = self.client.post(url, {
			'username': 'test_username',
			'phone': '12345678900',
			'password1': 'qweqwe876293e',
			'password2': 'qweqwe876293e'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Profile.objects.last().user.username, 'test_username')
