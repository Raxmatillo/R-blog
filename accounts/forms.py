from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password1', 'password2'
        ]

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name',]


class ProfileUpdateForm(forms.ModelForm):
    description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'description']