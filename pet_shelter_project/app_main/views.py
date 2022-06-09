from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SendMessageForm
from pet_shelter_project.settings import RECIPIENTS_EMAIL, EMAIL_HOST_USER
import logging

logger = logging.getLogger(__name__)


def main(request):
	return render(request, 'index.html')


def contacts(request):
	if request.method == 'GET':
		send_message_form = SendMessageForm()
		return render(request, 'contacts.html', context={'send_message_form': send_message_form})
	if request.method == 'POST':
		send_message_form = SendMessageForm(request.POST)
		if send_message_form.is_valid():
			name = send_message_form.cleaned_data['name']
			from_email = send_message_form.cleaned_data['from_email']
			message = send_message_form.cleaned_data['message']
			try:
				send_mail(f'от {name} {from_email}', message, EMAIL_HOST_USER, RECIPIENTS_EMAIL)
			except BadHeaderError:
				return HttpResponse('Ошибка')
			return redirect('/')
		return render(request, 'contacts.html', context={'send_message_form': send_message_form})
