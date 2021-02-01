from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(help_text='')
    email = forms.EmailField(label='Email', help_text='Provide your email')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput, help_text='Password must be at least 8 characters long')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    facebook = forms.URLField(initial='https://facebook.com/')
    twitter = forms.URLField(initial='https://twitter.com/')
    linkedin = forms.URLField(initial='https://linkedin.com/')

    class Meta:
        model = Profile
        fields = ['photo', 'facebook', 'twitter', 'linkedin']
