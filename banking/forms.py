from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import NumberInput

from .models import User, Transcations
from django.contrib.auth import authenticate
from .constants import USER_TYPES


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'user_type', 'account_type', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'{email} already Exist')


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Login')
        

class TranscationForm(forms.ModelForm):

    class Meta:
        model = Transcations
        fields = ['amount', 'Transcation_type']

class ExportForm(forms.ModelForm):
    start_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Transcations
        fields = ['user', 'start_date', 'end_date']