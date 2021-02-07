from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


class RegistrationView(SuccessMessageMixin, CreateView):
    """Register a new user."""
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('posts:index')
    success_message = '%(user)s Your Account Has Successfully Created!'
    extra_context = {'title': 'Register'}

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, user=self.object.username)


class ProfileView(LoginRequiredMixin, TemplateView, View):
    """User's Profile"""
    template_name = 'users/profile.html'

    def get_user_formset(self, data=None):
        return UserUpdateForm(instance=self.request.user, data=data)

    default_data = {
        'facebook': 'https://facebook.com/',
        'twitter': 'https://twitter.com/',
        'linkedin': 'https://linkedin.com/'
    }

    def get_profile_formset(self, data=None, files=None):
        return ProfileUpdateForm(instance=self.request.user.profile, data=data, files=files, initial=self.default_data)

    def get(self, request, *args, **kwargs):
        user_formset = self.get_user_formset()
        profile_formset = self.get_profile_formset()
        return self.render_to_response({
            'user_form': user_formset,
            'profile_form': profile_formset,
            'title': 'Profile'
        })

    def post(self, request, *args, **kwargs):
        user_formset = self.get_user_formset(data=request.POST)
        profile_formset = self.get_profile_formset(data=request.POST, files=request.FILES)

        if user_formset.is_valid() and profile_formset.is_valid():
            user_formset.save()
            profile_formset.save()
            messages.success(request, 'Your Account is Updated!!!')
            return HttpResponseRedirect('/profile/')
        return self.render_to_response({
            'user_form': user_formset,
            'profile_form': profile_formset,
            'title': 'Profile'
        })


class UserLoginView(SuccessMessageMixin, LoginView):
    """User login view"""
    extra_context = {'title': 'Login'}
    template_name = 'users/login.html'
    success_message = 'Login Successful'


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('posts:index')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """User logout view"""
    success_message = 'Logged Out'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Logged Out')
        return super(UserLogoutView, self).post(request, *args, **kwargs)
