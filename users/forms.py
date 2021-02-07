from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """Form to register a new user."""
    username = forms.CharField(help_text='')
    email = forms.EmailField(label='Email', help_text='Provide your email')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput, help_text='Password must be at least 8 characters long')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        cd_email = self.cleaned_data.get('email')
        if User.objects.filter(email=cd_email).exists():
            raise ValidationError('Email already exists.')
        return cd_email


class UserUpdateForm(forms.ModelForm):
    """Form to update a user's username and email."""
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form to update a user's image and social network links."""
    photo = forms.ImageField()
    facebook = forms.URLField(widget=forms.URLInput, help_text='https://facebook.com/', error_messages={'required': 'this is required'})
    twitter = forms.URLField(widget=forms.URLInput, help_text='https://twitter.com/', error_messages={'required': 'https://twitter.com/'})
    linkedin = forms.URLField(widget=forms.URLInput, help_text='https://linkedin.com/', error_messages={'required': 'https://linkedin.com/'})

    class Meta:
        model = Profile
        fields = ['photo', 'facebook', 'twitter', 'linkedin']
