from django.shortcuts import render
import logging


logger = logging.getLogger(__name__)

def main(request):
	return render(request, 'index.html')


def contacts(request):
	return render(request, 'contacts.html')