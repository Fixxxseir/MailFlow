from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "message_subject",
            "message_body",
        ]
        widgets = {
            "message_subject": forms.TextInput(attrs={"class": "form-control"}),
            "message_body": forms.Textarea(attrs={"class": "form-control"}),
        }
