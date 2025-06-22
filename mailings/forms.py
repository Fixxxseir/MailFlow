from django import forms
from .models import Mailing, Message, Recipient


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'start_sent_mailing', 'stop_sent_mailing', 'mailing_status']
        widgets = {
            'start_sent_mailing': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'stop_sent_mailing': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'mailing_status': forms.Select(attrs={'class': 'form-control'}),
        }
