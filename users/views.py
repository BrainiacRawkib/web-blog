from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


UserModel = get_user_model()


class RegistrationView(SuccessMessageMixin, View):
    """Register a new user."""
    success_message = '%(user)s Your Account Has Successfully Created!'

    def get(self, request):
        context = {
            'title': 'Register',
            'form': UserRegistrationForm()
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account.'
            activation_context = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            }
            # msg = render_to_string('users/activate_account.html', activation_context)
            msg = get_template('users/activate_account.html').render(activation_context)
            to_email = user.email
            send_email = EmailMessage(mail_subject, msg, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()
            messages.info(request, 'Please Confirm Your Email Address.')
            return redirect('posts:index')
        context = {
            'title': 'Register',
            'form': form
        }
        return render(request, 'users/register.html', context)


class ActivateAccountView(TemplateView, View):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(self.kwargs.get('uidb64')).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, self.kwargs.get('token')):
            user.is_active = True
            user.save()
            messages.success(request, 'Account Activated Successfully. You Can Now Login')
            return redirect('users:login')
        else:
            messages.error(request, 'Invalid Activation Link')
            return redirect('users:register')


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
