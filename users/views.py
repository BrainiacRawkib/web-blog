from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth import views as auth_views
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
    default_data = {
        'facebook': 'https://facebook.com/',
        'twitter': 'https://twitter.com/',
        'linkedin': 'https://linkedin.com/'
    }

    def get_user_formset(self, data=None):
        return UserUpdateForm(instance=self.request.user, data=data)

    def get_profile_formset(self, data=None, files=None):
        profile_formset = ProfileUpdateForm(instance=self.request.user.profile, data=data, files=files)
        # profile_formset['photo'].label_tag(attrs={'class': 'custom-file-label'})
        return profile_formset

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'user_form': self.get_user_formset(),
            'profile_form': self.get_profile_formset(),
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


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    """User login view"""
    extra_context = {'title': 'Login'}
    template_name = 'users/login.html'
    success_message = 'Login Successful'


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('posts:index')


class UserLogoutView(SuccessMessageMixin, auth_views.LogoutView):
    """User logout view"""
    success_message = 'Logged Out'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Logged Out')
        return super(UserLogoutView, self).post(request, *args, **kwargs)


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'users/passwords/password_change.html'
    extra_context = {'title': 'Password Change'}
    success_url = '/password-change/done/'


class ChangePasswordDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'users/passwords/password_change_done.html'
    extra_context = {'title': 'Password Changed Done'}


class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'users/passwords/password_reset.html'
    extra_context = {'title': 'Password Reset'}
    success_url = reverse_lazy('users:password-reset-done')
    email_template_name = 'users/passwords/password_reset_email.html'


class ResetPasswordDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/passwords/password_reset_done.html'
    extra_context = {'title': 'Password Reset Done'}


class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    extra_context = {'title': 'Confirm Password Reset'}
    success_url = reverse_lazy('users:password-reset-complete')
    template_name = 'users/passwords/password_reset_confirm.html'


class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/passwords/password_reset_complete.html'
    extra_context = {'title': 'Password Reset Complete'}
