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
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class': 'emailinput form-control mb-1'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form to update a user's image and social network links."""
    # photo = forms.ImageField(label='Choose file',
    #                          widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))
    photo = forms.ImageField(label='Choose file',
                             widget=forms.ClearableFileInput(attrs={'class': 'border'}))
    facebook = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control mb-1'}),
                              help_text='https://facebook.com/username/')
    twitter = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control mb-1'}),
                             help_text='https://twitter.com/username/')
    linkedin = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control mb-1'}),
                              help_text='https://linkedin.com/in/username/')

    class Meta:
        model = Profile
        fields = ['photo', 'facebook', 'twitter', 'linkedin']

    def clean_facebook(self):
        cd_facebook_url = self.cleaned_data.get('facebook')
        if len('https://facebook.com/') == len(cd_facebook_url) or len(cd_facebook_url) < len('https://facebook.com/'):
            raise ValidationError('Invalid Facebook username')
        return cd_facebook_url

    def clean_twitter(self):
        cd_twitter_url = self.cleaned_data.get('twitter')
        if len('https://twitter.com/') == len(cd_twitter_url) or len(cd_twitter_url) < len('https://twitter.com/'):
            raise ValidationError('Invalid Twitter username')
        return cd_twitter_url

    def clean_linkedin(self):
        cd_linkedin_url = self.cleaned_data.get('linkedin')
        if len('https://linkedin.com/') == len(cd_linkedin_url) or len(cd_linkedin_url) < len('https://linkedin.com/'):
            raise ValidationError('Invalid Linkedin username')
        return cd_linkedin_url
