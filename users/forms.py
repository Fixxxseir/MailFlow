from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.forms import BooleanField
from django.utils.deconstruct import deconstructible

# from catalog.forms import StyleProductMixin
from users.models import User


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=50, required=True)

	class Meta:
		model = User
		fields = ("email", "avatar", "username", "phone_number", "country", "password1", "password2")
		widgets = {}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["email"].widget.attrs.update({"placeholder": "Введите почту"})
		self.fields["username"].widget.attrs.update({"placeholder": "Введите никнейм"})
		self.fields["phone_number"].widget.attrs.update({"placeholder": "Введите номер телефона"})
		self.fields["country"].widget.attrs.update({"placeholder": "Введите ваш город"})
		self.fields["password1"].widget.attrs.update({"placeholder": "Введите ваш пароль"})
		self.fields["password2"].widget.attrs.update({"placeholder": "Введите ваш пароль повторно"})


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ("username", "phone_number", "country", "avatar")


class CustomPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={"class": "form-control form-control-user", "placeholder": "Введите ваш email"})
	)


class CustomLoginForm(AuthenticationForm):
	username = forms.CharField(
		label="Почта",
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите почту'})
	)
	password = forms.CharField(
		label="Пароль",
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
	)
