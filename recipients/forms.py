from django import forms

from .models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "first_name", "last_name", "comment"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control-file"}),
        }
