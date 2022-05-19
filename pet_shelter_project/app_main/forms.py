from django import forms
from django.utils.translation import gettext as _


class SendMessageForm(forms.Form):
    from_email = forms.EmailField(label=_('Email'), required=True, help_text='Email')
    name = forms.CharField(label=_('Имя'), required=True)
    message = forms.CharField(label=_('Сообщение'), widget=forms.Textarea, required=True)
